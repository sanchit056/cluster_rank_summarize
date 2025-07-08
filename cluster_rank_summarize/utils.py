from typing import Dict, List, Tuple, Optional
import pandas as pd
from typing import Dict, List, Union, TypedDict
from enum import Enum

class RankingFeedback(Enum):
    PROMOTE = "promote"
    DEMOTE = "demote"

# -------------------------------------------------------------------
# collect_ranking_feedback:
#   Collect ranking feedback from the user via the CLI.
#
#   Returns a list of indices representing the user's ranking 
#   (with the first index being the highest ranked itemset).
# -------------------------------------------------------------------
def collect_ranking_feedback(pruned_itemsets: pd.DataFrame) -> Optional[List[int]]:
    """Collect ranking feedback from user."""
    while True:
        ranking_input = input("Your ranking: ").strip()
        ranking_order = [int(x.strip()) for x in ranking_input.split(",") if x.strip().isdigit()]
        if not ranking_order:
            return None
        if len(ranking_order) == len(pruned_itemsets):
            return ranking_order
        print(f"Invalid ranking: You provided {len(ranking_order)} indices, but there are {len(pruned_itemsets)} itemsets.")
        print("Please try again. Note that you may hit <Enter> if the default ranking is satisfactory")

def collect_itemset_feedback(pruned_itemsets: pd.DataFrame) -> Optional[List[int]]:
    """
    Collect individual itemset feedback from user and return reordered ranking.
    
    Returns:
        List of itemset indices representing the new ranking order, or None if no feedback
    """
    # Start with current ranking order (0, 1, 2, ...)
    current_ranking = list(range(len(pruned_itemsets)))
    promoted_items = []
    demoted_items = []
    
    print("\nProvide feedback for individual itemsets:")
    print("Format: <itemset_id> <action>")
    print("Actions: promote, demote")
    print("Example: 0 promote")
    print("Example: 2 demote")
    print("Type 'done' when finished, or press Enter to skip feedback.")
    
    while True:
        user_input = input("Feedback: ").strip()
        
        if user_input.lower() == 'done' or user_input == '':
            break
            
        try:
            parts = user_input.split()
            if len(parts) != 2:
                print("Invalid format. Use: <itemset_id> <action>")
                continue
                
            itemset_id = int(parts[0])
            action_str = parts[1].lower()
            
            if itemset_id < 0 or itemset_id >= len(pruned_itemsets):
                print(f"Invalid itemset_id {itemset_id}. Must be between 0 and {len(pruned_itemsets)-1}")
                continue
                
            if action_str == RankingFeedback.PROMOTE.value:
                if itemset_id not in promoted_items:
                    promoted_items.append(itemset_id)
                    print(f"Added: Promote itemset {itemset_id}")
                else:
                    print(f"Itemset {itemset_id} is already promoted")
            elif action_str == RankingFeedback.DEMOTE.value:
                if itemset_id not in demoted_items:
                    demoted_items.append(itemset_id)
                    print(f"Added: Demote itemset {itemset_id}")
                else:
                    print(f"Itemset {itemset_id} is already demoted")
            else:
                print(f"Invalid action '{action_str}'. Use '{RankingFeedback.PROMOTE.value}' or '{RankingFeedback.DEMOTE.value}'")
                continue
                
        except ValueError:
            print("Invalid itemset_id. Must be a number.")
            continue

    if not promoted_items and not demoted_items:
        return None

    remaining_items = [item for item in current_ranking 
                      if item not in promoted_items and item not in demoted_items]

    new_ranking = promoted_items + remaining_items + demoted_items
    
    print(f"\nRanking updated:")
    print(f"Promoted items: {promoted_items}")
    print(f"Demoted items: {demoted_items}")
    print(new_ranking)
    
    return new_ranking

# Define TypedDict for the enriched itemset structure
class EnrichedItemset(TypedDict):
    itemset: Dict[str, str]  # Column name to value mapping
    # The second key is dynamic (row_id_colname) with a list of IDs

# Type alias for the column groups dictionary
ColumnGroupDict = Dict[str, List[Dict[str, Union[Dict[str, str], List[Union[int, str]]]]]]

def group_itemsets_by_columns(
    filtered_details_list: List[Dict[str, str]],
    pruned_itemsets: pd.DataFrame,
    row_id_colname: str = ''
) -> Tuple[ColumnGroupDict, ColumnGroupDict, ColumnGroupDict]:
    """
    Group itemsets by their column names.
    
    Args:
        filtered_details_list: List of dictionaries with column-value pairs
        pruned_itemsets: DataFrame containing the original itemsets with row IDs
        row_id_colname: Name of the column containing row IDs
        
    Returns:
        Tuple of three dictionaries (very_interesting, mildly_interesting, uninteresting)
        Each dictionary maps column patterns to lists of enriched itemsets
    """
    column_groups = {}
    
    for idx, itemset in enumerate(filtered_details_list):
        # Get sorted list of column names for this itemset
        columns = sorted(itemset.keys())
        # Create consistent key regardless of column order
        column_key = "|".join(columns)
        
        # Initialize list if key doesn't exist
        if column_key not in column_groups:
            column_groups[column_key] = []
        
        # Get the row IDs for this itemset
        row_ids = []
        if row_id_colname and idx < len(pruned_itemsets) and row_id_colname in pruned_itemsets.iloc[idx]:
            row_ids = pruned_itemsets.iloc[idx][row_id_colname]
        
        # Add both the itemset details and row IDs to the group
        enriched_itemset = {
            'itemset': itemset,
            row_id_colname: row_ids
        }
        
        column_groups[column_key].append(enriched_itemset)
    
    # Split into three categories
    very_interesting_itemsets = {}
    mildly_interesting_itemsets = {}
    uninteresting_itemsets = {}
    
    for key, itemsets in column_groups.items():
        group_size = len(itemsets)
        if group_size == 1:
            very_interesting_itemsets[key] = itemsets
        elif group_size == 2:
            mildly_interesting_itemsets[key] = itemsets
        else:  # 3 or more
            uninteresting_itemsets[key] = itemsets
    
    return very_interesting_itemsets, mildly_interesting_itemsets, uninteresting_itemsets