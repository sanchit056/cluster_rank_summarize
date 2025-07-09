# Cluster Rank Summarize Framework 🎯

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

**Cluster Rank Summarize** is an intelligent data clustering framework that combines advanced itemset mining, hierarchical clustering, and LLM-powered analysis to discover meaningful patterns in complex datasets. Built for researchers, data scientists, and analysts who need to uncover hidden insights from tabular data.

## ✨ Key Features

- **🔍 Intelligent Itemset Mining**: Discover frequent patterns with configurable support thresholds
- **📊 Hierarchical Clustering**: Automatically group similar itemsets with customizable similarity thresholds
- **🤖 LLM-Enhanced Analysis**: Generate human-readable summaries of itemsets as well as their categorization, advanced cluster     analysis and insights using AI
- **⚡ Interactive Training**: Iteratively improve clustering results with user feedback
- **📈 Rich Visualizations**: Create interactive sunburst charts, network graphs, and heatmaps
- **🎯 Similarity Search**: Find similar itemsets and clusters for targeted analysis
- **⚙️ Flexible Configuration**: Customize weights, parameters, and ranking strategies

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/radiantlogicinc/cluster_rank_summarize.git
cd clustering-project

# Install the package
pip install -e .

# Set up environment variables
mkdir -p env
cp .env.example env/.env
# Edit env/.env with your configuration (database path, API keys, etc.)
```

### Setting Up the Database and Running the Pipeline

The framework works with SQLite databases. After installation:

1. **Prepare your SQLite database** with your tabular data
2. **Configure environment variables** in `env/.env`:
   DB_PATH=/path/to/your/database.db
   LITELLM_API_KEY_SUMMARIZATION=your_api_key_here  # Optional, for LLM features
3. **Run the main script**:
   ```bash
   python cluster_rank_summarize/main.py train    # First time training
   python cluster_rank_summarize/main.py cluster  # Generate clusters
   ```

The script will automatically:
- Connect to your SQLite database
- Show available tables for selection
- Display column information for row ID selection
- Guide you through the clustering process

**Important: Row ID Column Selection**
When prompted, select a column that serves as a unique identifier for each row (e.g., `id`, `patient_id`, `record_id`). This column is essential for:
- Creating itemsets that group related data points
- Tracking which rows belong to which clusters
- Enabling similarity search and analysis
- Generating meaningful visualizations

The row ID column should contain unique values for each row in your dataset.

### Basic Custom Usage as a Package

If you want to use the framework as a package in your own applications, you can install it directly from GitHub:

```bash
# Install using uv (recommended)
uv pip install git+https://github.com/radiantlogicinc/cluster_rank_summarize.git

# Or install using pip
pip install git+https://github.com/radiantlogicinc/cluster_rank_summarize.git
```

After installation, you can import and use the framework in your Python applications:

```python
from cluster_rank_summarize.main import train, get_clusters
from cluster_rank_summarize.data_preprocessing import prepare_data
import polars as pl
import pandas as pd

# Load your tabular data
df = pl.read_csv("your_data.csv")

# Step 1: Process the polars dataframe and prepare the pandas dataframe
TD = prepare_data(df, row_id_colname="id")

# Step 2: Train the model with your preferences
train(df, row_id_colname="id", table_name="your_table")

# Step 3: Get clustering results
get_clusters(
    df, 
    row_id_colname="id",
    table_name="your_table",
    generate_visualizations=True,
    generate_advanced_report=True
)
```

### Command Line Interface

```bash
# Train the model interactively
python cluster_rank_summarize/main.py train

# Generate basic clustering results
python cluster_rank_summarize/main.py cluster

# Generate clusters with all advanced features
python cluster_rank_summarize/main.py cluster --visualize --advanced --itemset_summarization_categorization

# Optimize learning rate parameters (advanced users)
python cluster_rank_summarize/main.py tune_lr
```

### Command Line Flags

The framework supports several optional flags to enhance your analysis:

| Flag | Description | Requirements |
|------|-------------|--------------|
| `--advanced` | Generate comprehensive cluster analysis reports with executive summaries, detailed analysis of all clusters, comparitive analysis of clusters and actionable insights | Requires API key |
| `--visualize` | Create interactive visualizations including sunburst charts, network graphs, heatmaps, and dendrograms | Requires API key for itemset summaries |
| `--itemset_summarization_categorization` | Generate human-readable summaries of itemsets and categorize them by interest level | Requires API key |

**Example Usage:**
```bash
# Basic clustering without LLM features
python cluster_rank_summarize/main.py cluster

# Full analysis with all features (requires API key)
python cluster_rank_summarize/main.py cluster --advanced --visualize --itemset_summarization_categorization

# Just visualizations
python cluster_rank_summarize/main.py cluster --visualize

# Just itemset summarization and categorization by LLM
python cluster_rank_summarize/main.py cluster --itemset_summarization_categorization

# Just advanced cluster analysis
python cluster_rank_summarize/main.py cluster --advanced
```

**Note:** Features requiring API keys will prompt you to enter your API key if not configured in the environment file.

### Operation Modes

The framework supports three main operation modes:

| Mode | Purpose | Description |
|------|---------|-------------|
| `train` | Initial Training | Interactive training mode where you review itemsets and provide feedback to improve clustering results. Creates/updates configuration files. |
| `cluster` | Generate Results | Uses trained configuration to generate clustering results, visualizations, and analysis reports. |
| `tune_lr` | Parameter Optimization | Advanced mode for testing different learning rate combinations to find optimal parameters. |

**Typical Workflow:**
1. **First-time setup**: Run `train` mode to set preferences and create configuration
2. **Generate results**: Run `cluster` mode with desired flags for analysis
3. **Optimize parameters** (optional): Run `tune_lr` mode to fine-tune learning rates
4. **Iterate**: Re-run `train` mode if results need improvement

## 🎯 Use Cases

- **Market Research**: Segment customers and discover behavioral patterns
- **Operational Analysis**: Find process inefficiencies and optimization opportunities
- **Academic Research**: Explore complex datasets for publication-ready insights

## 📁 Project Structure

```
cluster_rank_summarize/
├── main.py                    # Entry point and CLI interface
├── clustering.py              # Hierarchical clustering algorithms
├── data_preprocessing.py      # Data cleaning and preparation
├── itemset_mining.py          # Frequent itemset mining and algorithms
├── llm_analysis.py            # AI-powered analysis and summarization
├── parameter_optimization.py  # Learning rate and weight optimization
├── similarity_search.py       # Similarity computation and search
├── visualization.py           # Interactive charts and graphs
├── display_utils.py           # Output formatting and display
└── utils.py                   # Helper functions and utilities
```

## 🔧 Configuration

The framework uses JSON configuration files stored in `ranking_config/` to persist your preferences:

```json
{
    "weights": {
        "column1": 0.3,
        "column2": 0.2,
        "column3": 0.5
    },
    "min_support": 0.1,
    "max_collection": -1,
    "gamma": 0.7,
    "lr_weights": 0.12,
    "lr_gamma": 0.8
}
```

## 🎨 Demo

The `demo/` folder contains a complete example using the MIMIC-III dataset:

**Demo Contents:**
- `ADMISSIONS.csv`: Sample medical admissions data
- `ADMISSIONS_config.json`: Pre-trained configuration
- `cluster_reports/`: Detailed analysis reports for each cluster
- `cluster_sunburst_with_summary.html`: Interactive visualization with a complete hierarchy
- `itemset_summaries.md`: Human-readable itemset descriptions

## 🤖 AI-Powered Features

### LLM Integration
- **Itemset Summarization**: Convert complex patterns into readable descriptions
- **Interest Categorization**: Automatically classify patterns by relevance
- **Advanced Analysis**: Generate executive summaries and actionable insights of clusters

### Supported Models
- DeepSeek API (default)
- OpenAI GPT models
- Any LiteLLM-compatible endpoint

## 📊 Visualization Gallery

- **Sunburst Charts**: Interactive hierarchical cluster visualization
- **Network Graphs**: Cluster relationships and connections
- **Heatmaps**: Similarity matrices and overlap analysis
- **Dendrograms**: Hierarchical clustering trees

## 🔍 Advanced Features

### Similarity Search
```python
# Find similar itemsets
similarities = get_similar_itemsets(itemsets, itemset_id=5, row_id_colname="id", top_n=10)

# Find similar clusters
cluster_similarities = get_similar_clusters(clusters, cluster_id=2, itemsets=itemsets, row_id_colname="id", top_n=5)
```

### Parameter Optimization
```python
# Test different learning rate combinations
results = test_learning_rate_combinations(dataframe, row_id_colname)
```

### Interactive Training
The framework supports iterative improvement through user feedback:
1. Review initial clustering results
2. Promote/demote itemsets based on relevance
3. Automatically adjust weights and parameters
4. Re-cluster with improved settings

## 📋 Requirements

- Python 3.11+
- pandas >= 2.2.3
- polars >= 1.30.0
- scikit-learn (via mlxtend)
- plotly >= 6.1.2
- networkx >= 3.4.2
- litellm >= 1.74.0 (for LLM features)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

**Ready to discover hidden patterns in your data?** Start with our [Quick Start Guide](#-quick-start) and explore the demo!