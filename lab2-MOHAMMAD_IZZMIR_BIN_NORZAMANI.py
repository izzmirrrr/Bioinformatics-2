import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

#retrieve PPI data from BioGRID 
def retrieve_ppi_biogrid(target_protein):
    data = {'Protein1': [target_protein, target_protein], 'Protein2': ['ProteinB', 'ProteinC']}
    df = pd.DataFrame(data)
    return df

# retrieve PPI data from STRING 
def retrieve_ppi_string(target_protein):
    data = {'Protein1': [target_protein, target_protein], 'Protein2': ['ProteinX', 'ProteinY']}
    df = pd.DataFrame(data)
    return df

# generate network graph
def generate_network(dataframe):
    G = nx.Graph()
    for _, row in dataframe.iterrows():
        G.add_edge(row['Protein1'], row['Protein2'])
    return G

# calculate centrality measures
def get_centralities(network_graph):
    centralities = {
        'degree': nx.degree_centrality(network_graph),
        'betweenness': nx.betweenness_centrality(network_graph),
        'closeness': nx.closeness_centrality(network_graph),
        'eigenvector': nx.eigenvector_centrality(network_graph),
        'pagerank': nx.pagerank(network_graph)
    }
    return centralities

# Title
st.title("Protein-Protein Interaction Network")


# user input
protein_id = st.text_input("Enter Protein ID:")
database_choice = st.selectbox("Choose Database", ["BioGRID", "STRING"])

# Run when the button is pressed
if st.button("Retrieve PPI Data"):
    if database_choice == "BioGRID":
        ppi_data = retrieve_ppi_biogrid(protein_id)
    else:
        ppi_data = retrieve_ppi_string(protein_id)

    # Display PPI data information
    st.subheader("PPI Data Information")
    st.write(ppi_data)
    st.write(f"Number of edges: {ppi_data.shape[0]}")
    st.write(f"Number of nodes: {ppi_data['Protein1'].nunique() + ppi_data['Protein2'].nunique()}")

    # Generate and display the network graph using matplotlib
    network_graph = generate_network(ppi_data)
    st.subheader("Network Visualization")
    fig, ax = plt.subplots()
    nx.draw(network_graph, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, ax=ax)
    st.pyplot(fig)

    # Calculate and display centrality measures
    st.subheader("Centrality Measures")
    centralities = get_centralities(network_graph)
    st.write(centralities)
