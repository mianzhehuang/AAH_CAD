# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 12:59:35 2024

@author: huang
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

# Set Streamlit page configuration
st.set_page_config(
    page_title="Alliance Animal Health Competitive Analysis",
    layout="wide",  # Makes the dashboard use the full width of the screen
    initial_sidebar_state="expanded"  # Expands the sidebar by default
)

# Title for the dashboard
st.title("Alliance Animal Health Competitive Analysis Dashboard [Prototype]")

# Define options and their availability
options = {
    "Veterinary Practice Partners": True,
    "All": False,
    "Nebraska Animal Medical and Emergency Center": False,
    "Victor Medical Company": False,
    "VCA Animal Hospitals": False,
    "Mission Veterinary Partners": False,
}

# Create a list of display names for the selectbox
display_options = [
    f"(Unavailable) {name}" if not available else name
    for name, available in options.items()
]

# Add the competitor selection dropdown
selected_display_option = st.sidebar.selectbox("Select a competitor for benchmarking Alliance Animal Health", display_options)

# Add the note in red
st.sidebar.markdown(
    """
    <span style="color:red;"><strong>Note:</strong> [Prototype] version ONLY incorporates Veterinary Practice Partner data for demonstration purposes.</span>
    """,
    unsafe_allow_html=True
)

# Custom CSS for Font Size
st.markdown(
    """
    <style>
    .custom-font {
        font-size: 21px;
        line-height: 1.6; /* Adjust line spacing for better readability */
    }
    .custom-font ul {
        margin-left: 20px; /* Indent the bullet points */
    }
    .custom-font li {
        font-size: 21px; /* Ensure list items inherit the font size */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Dashboard Purpose and Insights
st.markdown("### Section I. Dashboard purpose and strategic objectives")
st.markdown(
    """
    <div class="custom-font">
    This dashboard is designed to provide actionable 
    insights for strategic decision-making by evaluating Alliance Animal Health's competitive position 
    within the veterinary services market. By leveraging advanced AI-driven tools and techniques, the dashboard 
    consolidates critical data, such as geographic presence, customer reviews, accreditation statuses, 
    and regional demographics.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("#### With this dashboard, users can:")
st.markdown(
    """
    <div class="custom-font">
    <ul>
        <li><strong>Understand Competitive Dynamics</strong>: Analyze Alliance's strengths and weaknesses compared to key competitors in 
            various regions across the United States.</li>
        <li><strong>Identify Opportunities</strong>: Uncover underserved markets, customer pain points, and areas for operational improvements.</li>
        <li><strong>Visualize Strategies</strong>: Gain a regional perspective on performance metrics and strategic priorities.</li>
        <li><strong>Enhance Decision-Making</strong>: Use AI-driven insights from customer reviews to recommend strategies for boosting 
            customer satisfaction and efficiency.</li>
    </ul>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="custom-font">
    This tool ultimately aims to support Alliance Animal Health in capturing more market share, addressing sector 
    complexities, and driving value creation through targeted, data-backed initiatives.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---") 

# Data Pipeline
st.markdown("### Section II. Build an AI-driven data pipeline for competitive insights")

# Content
st.markdown(
    """
    <div class="custom-font">
    Rich public datasets, such as customer reviews and hospital locations, provide opportunities for AI-driven insights. 
    However, much of this data is unstructured, requiring sophisticated tools and techniques for extraction and transformation.</br>
    To address this challenge, a data pipeline was designed leveraging web scraping AI tools like 
    <strong>FireCrawl</strong>, <strong>JINA AI</strong>, and <strong>Instant Data Scraper</strong> for data extraction. 
    Data transformation is handled using <strong>Python</strong>, <strong>LangChain</strong>, and <strong>OpenAI</strong>, 
    with all processed data stored in <strong>Google BigQuery</strong>. The pipeline operates on a monthly schedule to ensure timely updates.
    </div>
    """,
    unsafe_allow_html=True
)

# Data Highlights
st.markdown(
    """
    <div class="custom-font">
    <strong>Data Warehouse Highlights:</strong>
    <ul>
        <li><strong>350+ Veterinary Hospitals</strong>: Includes hospital names and locations.</li>
        <li><strong>100K+ Google Customer Reviews</strong>: Comprehensive review data for each hospital.</li>
        <li><strong>Review Analysis</strong>: Extracted and summarized insights at both hospital and regional levels.</li>
    </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# Insert a PNG file
st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Centralized title
st.markdown(
    """
    <div class="centered-title">
    Data Pipeline Diagram
    </div>
    """,
    unsafe_allow_html=True
)

st.image("etl_vet_hospitals.drawio.png", use_container_width=True) #caption="Data Pipeline Diagram",


st.markdown("---") 

# Metrics
st.markdown("### Section III. Visualize Alliance's performance metrics to uncover underserved regions and drive improvement")


# Map the selected display option back to the original option name
selected_option = selected_display_option.replace("(Unavailable) ", "")

# Add reference link
st.sidebar.markdown(
    "**Reference:** [Alliance Animal Health Competitor Information](https://compworth.com/company/alliance-animal-health)"
)

# Dropdown Menu for Region Selection
st.sidebar.header("Region Level Comparison")
regions = [
    "All",
    "New England",
    "Mid-Atlantic",
    "East North Central",
    "West North Central",
    "South Atlantic",
    "East South Central",
    "West South Central",
    "Mountain",
    "Pacific",
    
]

regions_explanation = {
    "All": ["",""],
    'New England': [
        'Maine, Vermont, New Hampshire, Massachusetts, Connecticut, Rhode Island.',
        'This region, comprising states in the northeastern corner of the U.S., is characterized by smaller geographic areas and higher population densities, leading to localized veterinary demand.'
    ],
    'Mid-Atlantic': [
        'New York, New Jersey, Pennsylvania.',
        "Located along the eastern seaboard, this region's diverse urban and rural areas create varied needs for veterinary services, including specialty care."
    ],
    'East North Central': [
        'Ohio, Indiana, Illinois, Michigan, Wisconsin.',
        'This area in the Midwest features significant agricultural activity, influencing the demand for both companion animal and livestock veterinary services.'
    ],
    'West North Central': [
        'Minnesota, Iowa, Missouri, North Dakota, South Dakota, Nebraska, Kansas.',
        'A largely rural region in the Midwest, the demand here is driven by agricultural practices and livestock health.'
    ],
    'South Atlantic': [
        'Delaware, Maryland, Washington D.C., Virginia, West Virginia, North Carolina, South Carolina, Georgia, Florida.',
        'Spanning the eastern coastline, this region has a mix of urban centers and rural areas, driving a need for diverse veterinary services.'
    ],
    'East South Central': [
        'Kentucky, Tennessee, Alabama, Mississippi.',
        'Known for its agricultural activities and rural landscape, this region has a strong focus on livestock and companion animal care.'
    ],
    'West South Central': [
        'Arkansas, Louisiana, Oklahoma, Texas.',
        'With its large land area and ranching culture, this region emphasizes livestock veterinary services alongside urban companion animal care.'
    ],
    'Mountain': [
        'Montana, Idaho, Wyoming, Nevada, Utah, Colorado, Arizona, New Mexico.',
        'Defined by its rugged terrain and rural character, the Mountain region sees a focus on both livestock and companion animals in sparsely populated areas.'
    ],
    'Pacific': [
        'Washington, Oregon, California, Alaska, Hawaii.',
        'This coastal region includes densely populated urban centers and agricultural areas, driving high demand for veterinary care across specialties.'
    ]
}


selected_region = st.sidebar.selectbox("Select Region", regions, index=0)

st.sidebar.markdown(
   '<span style="font-weight:bold; color:blue;">'+regions_explanation[selected_region][0]+"</span>"+ regions_explanation[selected_region][1],
   unsafe_allow_html=True
)



st.markdown("#### Key takeaways upon reviewing this section:")

#if selected_region=="All":
st.markdown(
    f"""
    <div class="custom-font">
    <ul>
        <li><strong>Underserved Regions</strong>: Compared to {selected_option}, Alliance is underserved in the <u>Mid-Atlantic region (New York, New Jersey, Pennsylvania)</u> and <u>Pacific especially California</u>. These areas feature high population densities, with urban centers showing elevated demand for <u>specialized veterinary care</u>.</li>
        <li><strong>Competitive Regions</strong>: Compared to {selected_option}, Alliance is competitive in the <u>Middle South regions</u>, which are less densely populated but primarily focused on livestock care.</li>       
        <li><strong>Strategic Improvements</strong>: 
            To better compete with {selected_option}, the following actions for Alliance are recommended:
            <ul>
                <li><strong>Mid-Atlantic Region:</strong>
                    <ul>
                        <li>Expand its presence in densely populated areas to address underserved markets.</li>
                        <li>Increase the number of accredited hospitals to meet the growing demand for specialized veterinary care.</li>
                    </ul>
                </li>
                <li><strong>California:</strong>
                    <ul>
                        <li>Enhance customer experience by addressing substantially lower Google ratings compared to {selected_option} (3.92 vs 4.62).</li>
                    </ul>
                </li>
            </ul>
        </li>
    </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# st.markdown(
#     f"""
#     <div class="custom-font">
#     <ul>
#         <li><strong>Underserved Regions</strong>: Compared to {selected_option}, Alliance is underserved in the <u>Mid-Atlantic region (New York, New Jersey, Pennsylvania)</u> and <u>Pacific especially California</u>. These areas feature high population densities, with urban centers showing elevated demand for <u>specialized veterinary care</u>.</li>
#         <li><strong>Competitive Regions</strong>: Compared to {selected_option}, Alliance is competitive in the <u>Middle South regions</u>, which are less densely populated but primarily focused on livestock care.</li>       
#         <li><strong>Strategic Improvements</strong>: To better compete with {selected_option}, Alliance should expand its presence in the densely populated Mid-Atlantic region and increase the number of accredited hospitals to meet the growing demand for specialized veterinary care. In California, Alliance needs to focus on enhancing customer experience, as its Google rating is significantly lower than that of {selected_option} (3.92 vs 4.62).</li>
#     </ul>
#     </div>
#     """,
#     unsafe_allow_html=True
# )


st.markdown("#### User guide for this section:")
# st.markdown(
#     """
#     <div class="custom-font">
#     <ul>
#         <li><strong>Competitor Selection</strong>: The first dropdown menu on the left-hand side enables you to select a competitor for <u>benchmarking</u> against Alliance Animal Health. Upon selection, the map displays both Alliance and the chosen competitor's hospitals across the United States.</li>
#         <li><strong>Regional Segmentation</strong>: The second menu divides the U.S. map into <u>9</u> distinct regions, each highlighting unique veterinary service trends. Selecting a region allows you to <u>zoom in</u> and explore detailed insights specific to that area.</li>       
#         <li><strong>Population Density Overlay</strong>: The map features a blue gradient overlay, with dark blue representing regions of high population density and light blue indicating lower-density areas, reflecting <u>potential demand</u> for veterinary services.</li>
#     </ul>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

st.markdown(
    """
    <div class="custom-font">
    <ul>
        <li><strong>Competitor Selection</strong>: The first dropdown menu on the left-hand side enables you to select a competitor for <u>benchmarking</u> against Alliance Animal Health. Upon selection, the map displays both Alliance and the chosen competitor's hospitals across U.S. <strong><span style="color:red;"> Note: [Prototype] version ONLY incorporates Veterinary Practice Partner data for demonstration purposes.</span></strong></li>
        <li><strong>Regional Segmentation</strong>: The second dropdown menu divides the U.S. map into <u>9</u> distinct regions from east to west, each highlighting unique veterinary service trends. Selecting a region allows you to <u>zoom in</u> and explore detailed insights specific to that area.</li>       
        <li><strong>Population Density Overlay</strong>: The map features a blue gradient overlay, with dark blue representing regions of high population density and light blue indicating lower-density areas, reflecting <u>potential demand</u> for veterinary services.</li>
        <li><strong>Metrics Display</strong>: Below the map, key metrics such as the total number of hospitals, number of accredited hospitals, average Google review ratings, and rankings are displayed for comparison between Alliance and the selected competitor.</li>
    </ul>
    </div>
    """,
    unsafe_allow_html=True
)



# Load data
us_density = pd.read_excel("us_density.xlsx")  # Ensure it has latitude, longitude, and density_category
aa_partners = pd.read_excel("vets_partners_aa_google_reviews.xlsx")  # Ensure correct columns
vet_reviews_details = pd.read_pickle(r"vet_reviews_details.pkl")




# Cache data loading
# @st.cache_data
# def load_data():
#     us_density = pd.read_parquet("us_density.parquet")
#     aa_partners = pd.read_parquet("vets_partners_aa_google_reviews.parquet")
#     #vvp_partners = pd.read_parquet("vets_partners_vvp_google_reviews.parquet")
#     vet_reviews_details = pd.read_pickle("vet_reviews_details.pkl")
#     return us_density, aa_partners, vet_reviews_details

# # Load data
# us_density, aa_partners, vvp_partners, vet_reviews_details = load_data()



# Normalize the density values for visualization
us_density["normalized_density"] = np.log1p(us_density["density_category"])


# Check if the selected option has data available
if options[selected_option]:
    st.write(f"Displaying data for Alliance Animal Health and {selected_option}")
else:
    st.warning(f"### Data for {selected_option} is currently unavailable. [Prototype] version ONLY incorporates Veterinary Practice Partner data for demonstration purposes. Please switch back to Veterinary Practice Partner.")


# Create the base map
fig = go.Figure()

# Add density points to the map (without hover info)
fig.add_trace(
    go.Scattergeo(
        lat=us_density["latitude"],
        lon=us_density["longitude"],
        marker=dict(
            size=4,
            color=us_density["density_category"],
            colorscale="Blues",
            showscale=True,
            colorbar=dict(title="Density Category"),
        ),
        hoverinfo="skip",  # Disable hover for density points
        name="",
    )
)

# Add orange dots for Alliance Animal Health partners
if selected_region == "All":
    aa_partners_region = aa_partners
else:
    aa_partners_region = aa_partners[aa_partners["Region"]==selected_region]

fig.add_trace(
    go.Scattergeo(
        lat=aa_partners_region["latitude"],
        lon=aa_partners_region["longitude"],
        # text=aa_partners.apply(
        #     lambda row: (
        #         f"<b>{row['Veterinary Partner Name']}</b><br>"
        #         f"<b>Rating:</b> {row['Rating']}/5<br>"
        #         f"<b>Total Reviews:</b> {row['Total Ratings #']}"
        #     ),
        #     axis=1,
        # ),
        text=aa_partners_region.apply(
            lambda row: (
                f"<span style='font-size:16px;'><b>{row['Veterinary Partner Name']}</b></span><br><br>"  # Extra <br> for spacing
                f"<span style='font-size:16px;'><b>Rating/#Reviews:</b> {row['Rating']}/{row['Total Ratings #']}</span>"
            ),
            axis=1,
        ),
        mode="markers",
        marker=dict(color="orange", size=8),
        name="Alliance Animal Health",
    )
)

# Add purple dots for competitors if selected
if selected_option == "Veterinary Practice Partners":
    vvp_partners = pd.read_excel("vets_partners_vvp_google_reviews.xlsx")  # Ensure correct columns
    if selected_region == "All":
        vvp_partners_region = vvp_partners
    else: 
        vvp_partners_region = vvp_partners[vvp_partners["Region"]==selected_region]
    fig.add_trace(
        go.Scattergeo(
            lat=vvp_partners_region["latitude"],
            lon=vvp_partners_region["longitude"],
            text=vvp_partners_region.apply(
                lambda row: (
                    f"<span style='font-size:16px;'><b>{row['Veterinary Partner Name']}</b></span><br><br>"  # Extra <br> for spacing
                    f"<span style='font-size:16px;'><b>Rating/#Reviews:</b> {row['Rating']}/{row['Total Ratings #']}</span><br>"
                ),
                axis=1,
            ),
            mode="markers",
            marker=dict(color="purple", size=8),
            name=selected_option,
        )
    )
    
    

# Update map layout
fig.update_layout(
    geo=dict(
        scope="usa",
        showland=True,
        landcolor="white",  # Set land color to white
        showlakes=False,    # Optional: Disable lakes
        showocean=False,    # Optional: Disable ocean             
    ),
    dragmode=False,  # Disable dragging/zooming
    title={
        "text": "US Veterinary Hospitals Presence based on Population Density",
        "x": 0.5,  # Center title
        "xanchor": "center",
        "yanchor": "top",
        "font": {"size": 20},  # Larger font for the title
    },
    height=800,
    margin={"r": 0, "t": 100, "l": 0, "b": 0},
    legend=dict(
        orientation="h",
        yanchor="top",
        y=0.92,  # Place the legend below the title
        xanchor="center",
        x=0.5,
        font=dict(size=14),
    ),
)

# Render the map in Streamlit
st.plotly_chart(fig, use_container_width=True)


#%% Section 2

vets_review = aa_partners
vets_review["Ratings*Reviews"] = vets_review['Total Ratings #'] * vets_review['Rating'] 
vets_sum1 = vets_review.groupby('Region')[["Veterinary Partner Name"]].nunique()
vets_sum2 = vets_review.groupby('Region')[['Total Ratings #', "Ratings*Reviews"]].sum()
vets_sum = pd.concat([vets_sum1, vets_sum2], axis=1)
vets_sum.reset_index(inplace=True)
vets_sum["Rating"] = vets_sum["Ratings*Reviews"] / vets_sum['Total Ratings #']
vets_sum.loc[len(vets_sum)] = ["All", 
                               sum(vets_sum['Veterinary Partner Name']), 
                               sum(vets_sum['Total Ratings #']), 
                               sum(vets_sum['Ratings*Reviews']),
                               sum(vets_sum['Ratings*Reviews'])/sum(vets_sum['Total Ratings #'])]


comp_vets_review = vvp_partners
comp_vets_review["Ratings*Reviews"] = comp_vets_review['Total Ratings #'] * comp_vets_review['Rating'] 
comp_vets_sum1 = comp_vets_review.groupby('Region')[["Veterinary Partner Name"]].nunique()
comp_vets_sum2 = comp_vets_review.groupby('Region')[['Total Ratings #', "Ratings*Reviews"]].sum()
comp_vets_sum = pd.concat([comp_vets_sum1, comp_vets_sum2], axis=1)
comp_vets_sum.reset_index(inplace=True)
comp_vets_sum["Rating"] = comp_vets_sum["Ratings*Reviews"] / comp_vets_sum['Total Ratings #']
comp_vets_sum.loc[len(vets_sum)] = ["All", 
                                   sum(comp_vets_sum['Veterinary Partner Name']), 
                                   sum(comp_vets_sum['Total Ratings #']), 
                                   sum(comp_vets_sum['Ratings*Reviews']),
                                   sum(comp_vets_sum['Ratings*Reviews'])/sum(comp_vets_sum['Total Ratings #'])]    

all_vets_review = pd.concat([vets_review[["Company", "Veterinary Partner Name", "Region", "Location", 'Total Ratings #', 'Rating', "AAHA Accreditation Status"]],
                        comp_vets_review[["Company", "Veterinary Partner Name", "Region", "Location", 'Total Ratings #', 'Rating', "AAHA Accreditation Status"]]])
region_bench = all_vets_review[["Region"]].drop_duplicates()
region_bench.loc[len(region_bench)] = ["All"]
vets_sum = pd.merge(region_bench, vets_sum, how="left", on="Region")
vets_sum.fillna(0, inplace=True)



all_vets_medium = all_vets_review[all_vets_review['Total Ratings #']>=100].groupby("Region")[['Rating']].median()
all_vets_medium.reset_index(inplace=True)
all_vets_medium.columns =["Region", "RatingMedium"]
all_vets_review = pd.merge(all_vets_review, all_vets_medium, how="left", on="Region")
all_vets_review["Top50%"] = all_vets_review.apply(lambda x: "Yes" if x["Rating"]>x["RatingMedium"] else "No", axis=1)

all_vets_review_aa = all_vets_review[all_vets_review["Company"]=="Alliance Animal Health"]
all_vets_review_comp = all_vets_review[all_vets_review["Company"]!="Alliance Animal Health"]



# Filter DataFrames Based on Region Selection
vets_filtered = (
    all_vets_review_aa
    if selected_region == "All"
    else all_vets_review_aa[all_vets_review_aa["Region"] == selected_region]
)
comp_vets_filtered = (
    all_vets_review_comp
    if selected_region == "All"
    else all_vets_review_comp[all_vets_review_comp["Region"] == selected_region]
)


col1, col2 = st.columns(2)

with col1:
    # Left-Hand Side Box: Alliance Animal Health Practitioners
    st.markdown(
        "<h2 style='color: orange;'>Alliance Animal Health - Metrics</h2>",
        unsafe_allow_html=True
    )
    
with col2:
    st.markdown(
        "<h2 style='color: purple;'>"+selected_option+" - Metrics</h2>",
        unsafe_allow_html=True
    )    
    
# 1. # Total Practitioners
total_practitioners_aa = int(vets_sum.loc[
    vets_sum["Region"] == selected_region, "Veterinary Partner Name"
].values[0])

total_accredited_aa_details = vets_filtered[(vets_filtered["AAHA Accreditation Status"] == "Yes")]
total_accredited_aa = len(total_accredited_aa_details)


# 2. Overall Rating / Total Reviews
rating_aa = vets_sum.loc[vets_sum["Region"] == selected_region, "Rating"].values[0]
total_reviews_aa = vets_sum.loc[
    vets_sum["Region"] == selected_region, "Total Ratings #"
].values[0]

# Format total_reviews_aa with commas
total_reviews_aa_formatted = f"{int(total_reviews_aa):,}"
with col1:
    # Display the Information
    st.markdown(f"#### Total Hospitals #: {total_practitioners_aa}")
    st.markdown(f"#### Accredited Hospitals #: {total_accredited_aa}")
    st.markdown(
        f"#### Google Rating / Reviews: {rating_aa:.2f} / {total_reviews_aa_formatted}"
    )

# 1. # Total Practitioners
total_practitioners_comp = comp_vets_sum.loc[
    comp_vets_sum["Region"] == selected_region, "Veterinary Partner Name"
].values[0]

total_accredited_comp_details = comp_vets_filtered[(comp_vets_filtered["AAHA Accreditation Status"] == "Yes")]
total_accredited_comp = len(total_accredited_comp_details)

# 2. Overall Rating / Total Reviews
rating_comp = comp_vets_sum.loc[
    comp_vets_sum["Region"] == selected_region, "Rating"
].values[0]
total_reviews_comp = comp_vets_sum.loc[
    comp_vets_sum["Region"] == selected_region, "Total Ratings #"
].values[0]

# Format total_reviews_comp with commas
total_reviews_comp_formatted = f"{int(total_reviews_comp):,}"

with col2:
    # Display the Information
    st.markdown(f"#### {total_practitioners_comp}")
    st.markdown(f"#### {total_accredited_comp}")    
    st.markdown(
        f"#### {rating_comp:.2f} / {total_reviews_comp_formatted}"
    )


st.markdown(f"### Rank all these {total_practitioners_aa} + {total_practitioners_comp} hospitals into four categories based on two criteria:")
# st.markdown(
#     """
#     <div class="custom-font">
#     <ul>
#         <li><strong>Criteria 1</strong>: The hospital is rated above top 50% among all the hospitals of Alliance and the selected competitor.</li>
#         <li><strong>Crtieria 2</strong>: The hospital has AAHA (American Animal Hospital Association) accreditation.</li>       
#         <li><strong>4 Categories</strong>: Tier 1 - the hospital meets both criterias; Tier 2 - ONLY meet Criteria 1; Tier 3- ONLY meet Crtieria 2; Tier 4 - Fails neither criterias.</li>
#     </ul>
#     </div>
#     """,
#     unsafe_allow_html=True
# )


st.markdown(
    """
    <div class="custom-font">
    <ul>
        <li><strong>Criteria 1</strong>: The hospital has a Google rating based on at least 50 reviews, ranking in the top 50% among all hospitals within Alliance and the selected competitor in the specified region.</li>
        <li><strong>Criteria 2</strong>: The hospital holds accreditation from the AAHA (American Animal Hospital Association).</li>       
        <li><strong>4 Categories</strong>: <strong>Tier 1</strong> - Meets both Criteria 1 and Criteria 2; <strong>Tier 2</strong> - Meets only Criteria 1; <strong>Tier 3</strong> - Meets only Criteria 2; <strong>Tier 4</strong> - Does not meet either criterion.</li>
    </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# st.markdown(
#     """
#     <div class="custom-font">
#     <ul>
#         <li><strong>Criteria 1</strong>: The hospital has a Google rating, based on at least 100 reviews, ranking in the top 50% among all hospitals within Alliance and the selected competitor.</li>
#         <li><strong>Criteria 2</strong>: The hospital holds accreditation from the AAHA (American Animal Hospital Association).</li>       
#         <li><strong>4 Categories</strong>: 
#             <ul>
#                 <li><strong>Tier 1</strong>: Meets both Criteria 1 and Criteria 2.</li>
#                 <li><strong>Tier 2</strong>: Meets only Criteria 1.</li>
#                 <li><strong>Tier 3</strong>: Meets only Criteria 2.</li>
#                 <li><strong>Tier 4</strong>: Does not meet either criterion.</li>
#             </ul>
#         </li>
#     </ul>
#     </div>
#     """,
#     unsafe_allow_html=True
# )    
    
st.markdown("**Reference:** [AAHA (American Animal Hospital Association) Accreditation.](https://www.aaha.org/for-pet-parents/find-an-aaha-hospital/) The only organization that accredits veterinary practices in the US and CA based on rigorous quality standards")

# Create Columns for Side-by-Side Layout
col3, col4 = st.columns(2)
# 3. Piechart for Alliance Animal Health Practitioners
if not vets_filtered.empty:
    vets_filtered = vets_filtered[["Veterinary Partner Name", "Location", "Rating","Top50%", "Total Ratings #", "AAHA Accreditation Status"]]
    top50_aa_aa_details = vets_filtered[
                            (vets_filtered["Top50%"] == "Yes")
                            & (vets_filtered["AAHA Accreditation Status"] == "Yes")
                        ].sort_values(by="Rating", ascending=False)
    
    top50_aa_aa = len(top50_aa_aa_details)
    
    top50_aa_no_details = vets_filtered[
                            (vets_filtered["Top50%"] == "Yes")
                            & (vets_filtered["AAHA Accreditation Status"] == "No")
                        ].sort_values(by="Rating", ascending=False)
    
    top50_aa_no = len(top50_aa_no_details)
    
    bottom50_aa_aa_details = vets_filtered[
            (vets_filtered["Top50%"] == "No")
            & (vets_filtered["AAHA Accreditation Status"] == "Yes")
        ].sort_values(by="Rating", ascending=False)
    
    bottom50_aa_aa = len(bottom50_aa_aa_details)
    
    bottom50_aa_no_details = vets_filtered[
            (vets_filtered["Top50%"] == "No")
            & (vets_filtered["AAHA Accreditation Status"] == "No")
        ].sort_values(by="Rating", ascending=True)
    
    bottom50_aa_no = len(bottom50_aa_no_details)
    
    
    all_details = pd.concat([top50_aa_aa_details, top50_aa_no_details,
                             bottom50_aa_aa_details, bottom50_aa_no_details])
    
    all_details.sort_values(by="Rating", inplace=True, ascending=False)


    # Additional data corresponding to each category
    details_mapping = {
        "Top50% & AAHA Accredited": top50_aa_aa_details,
        "Top50% & Not AAHA Accredited": top50_aa_no_details,
        "Bottom50% & AAHA Accredited": bottom50_aa_aa_details,
        "Bottom50% & Not AAHA Accredited": bottom50_aa_no_details,
        "All": all_details
    }
    
    
    # Percentages for Pie Chart
    total_aa = len(vets_filtered)
    pie_data_aa = {
        "Category": [
            #"Top50% & AAHA Accredited",
            #"Top50% & Not AAHA Accredited",
            #"Bottom50% & AAHA Accredited",
            #"Bottom50% & Not AAHA Accredited",
            "Tier 1",
            "Tier 2",
            "Tier 3",
            "Tier 4",
            
        ],
        "Count": [top50_aa_aa, top50_aa_no, bottom50_aa_aa, bottom50_aa_no],
        "Percentage": [
            (top50_aa_aa / total_aa) * 100,
            (top50_aa_no / total_aa) * 100,
            (bottom50_aa_aa / total_aa) * 100,
            (bottom50_aa_no / total_aa) * 100,
        ],
        "Color": ["darkblue", "blue", "lightblue", "white"],
    }    

    # Alliance Animal Health Practitioner Ratings Breakdown
    with col3:
        #st.subheader("Alliance Animal Health Practitioner Ratings")
        # Create the pie chart with explicit category order
        st.markdown("#### Among Alliance's hospitals,")

        pie_fig_aa = px.pie(
            pie_data_aa,
            names="Category",
            values="Count",
            color="Category",
            color_discrete_map={
                "Tier 1": "darkblue",
                "Tier 2": "blue",
                "Tier 3": "lightblue",
                "Tier 4": "white",
            },
            #title="Ratings & Accreditation Breakdown",
            category_orders={
                "Category": [
                    "Tier 1",
                    "Tier 2",
                    "Tier 3",
                    "Tier 4",
                ]
            },
        )
        st.plotly_chart(pie_fig_aa, use_container_width=True)
else:
    details_mapping = np.nan

# 3. Piechart for Competitor Practitioners
if not comp_vets_filtered.empty:
    comp_vets_filtered = comp_vets_filtered[["Veterinary Partner Name", "Location", "Rating","Top50%", "Total Ratings #", "AAHA Accreditation Status"]]
    
    top50_comp_aa_details = comp_vets_filtered[
            (comp_vets_filtered["Top50%"] == "Yes")
            & (comp_vets_filtered["AAHA Accreditation Status"] == "Yes")
        ].sort_values(by="Rating", ascending=False)
    
    top50_comp_aa = len(top50_comp_aa_details)
    
    top50_comp_no_details = comp_vets_filtered[
            (comp_vets_filtered["Top50%"] == "Yes")
            & (comp_vets_filtered["AAHA Accreditation Status"] == "No")
        ].sort_values(by="Rating", ascending=False)
    top50_comp_no = len(top50_comp_no_details)
    
    
    bottom50_comp_aa_details = comp_vets_filtered[
            (comp_vets_filtered["Top50%"] == "No")
            & (comp_vets_filtered["AAHA Accreditation Status"] == "Yes")
        ].sort_values(by="Rating", ascending=False)
    bottom50_comp_aa = len(bottom50_comp_aa_details)
    
    bottom50_comp_no_details = comp_vets_filtered[
            (comp_vets_filtered["Top50%"] == "No")
            & (comp_vets_filtered["AAHA Accreditation Status"] == "No")
        ].sort_values(by="Rating", ascending=True)
    bottom50_comp_no = len(bottom50_comp_no_details)
    
    all_details_comp = pd.concat([top50_comp_aa_details, top50_comp_no_details,
                                  bottom50_comp_aa_details, bottom50_comp_no_details])
    
    all_details_comp.sort_values(by="Rating", inplace=True, ascending=False)
    
    # Additional data corresponding to each category
    details_mapping_comp = {
        "Top50% & AAHA Accredited": top50_comp_aa_details,
        "Top50% & Not AAHA Accredited": top50_comp_no_details,
        "Bottom50% & AAHA Accredited": bottom50_comp_aa_details,
        "Bottom50% & Not AAHA Accredited": bottom50_comp_no_details,
        "All": all_details_comp
    }
    
    
    # Percentages for Pie Chart
    total_comp = len(comp_vets_filtered)
    pie_data_comp = {
        "Category": [
                    "Tier 1",
                    "Tier 2",
                    "Tier 3",
                    "Tier 4",
        ],
        "Count": [top50_comp_aa, top50_comp_no, bottom50_comp_aa, bottom50_comp_no],
        "Percentage": [
            (top50_comp_aa / total_comp) * 100,
            (top50_comp_no / total_comp) * 100,
            (bottom50_comp_aa / total_comp) * 100,
            (bottom50_comp_no / total_comp) * 100,
        ],
        "Color": ["darkblue", "blue", "lightblue", "white"],
    }
    
    # Competitor Practitioner Ratings Breakdown
    
    with col4:
        # Create the pie chart with explicit category order
        st.markdown(
            f"#### Among the {selected_option}'s hospitals,"
        )
        

        
        pie_fig_comp = px.pie(
            pie_data_comp,
            names="Category",
            values="Count",
            color="Category",
            color_discrete_map={
                "Tier 1": "darkblue",
                "Tier 2": "blue",
                "Tier 3": "lightblue",
                "Tier 4": "white",
            },
            #title="Ratings & Accreditation Breakdown",
            category_orders={
                "Category": [
                    "Tier 1",
                    "Tier 2",
                    "Tier 3",
                    "Tier 4",
                ]
            },
        )
        # Hide the legend
        #pie_fig_comp.update_layout(showlegend=False)
        st.plotly_chart(pie_fig_comp, use_container_width=True)
else:
    details_mapping_comp = np.nan

# Create Columns for Side-by-Side Layout
st.markdown("---")  # Optional horizontal rule for separation

# AI Analysis
st.markdown("### Section IV. OpenAI analyzes 100K+ reviews with improvement recommendations for Alliance vs. competitor in region level")


vets_reviews_region_sum = pd.read_pickle(r"vets_reviews_region_sum.pkl")
filtered_df = vets_reviews_region_sum[vets_reviews_region_sum['Region']==selected_region]

# Check if the region exists in the DataFrame
if not filtered_df.empty:
    # Extract the row corresponding to the selected region
    row = filtered_df.iloc[0]
    
    # Display the details using markdown
    #st.markdown(f"#### Based on customer reviews, is Alliance Animal Health better or worse than {selected_option}?")
    #st.markdown(f"#### For the specified region, OpenAI compares {total_reviews_aa_formatted} Google customer reviews of Alliance with {total_reviews_comp_formatted} reviews of {selected_option}, focusing on four key aspects. The assessment of Alliance's performance, benchmarked against {selected_option}, is summarized below:")
    st.markdown(
        f"""
        <div class="custom-font">
            <strong>For the specified region</strong>, OpenAI compares <strong>{total_reviews_aa_formatted}</strong> Google customer reviews of Alliance with <strong>{total_reviews_comp_formatted}</strong> reviews of {selected_option}, focusing on <strong>four key aspects</strong>. The assessment of Alliance's performance, benchmarked against {selected_option}, is summarized below:
        </div>
        """,
        unsafe_allow_html=True
    )

    me_judge, par, me_reason =  row['Medical Expertise'].partition('.')
    # Determine the color based on the value of me_judge
    if me_judge.strip() == "Worse":
        color = "red"
    elif me_judge.strip() == "Better":
        color = "green"
    else:
        color = "black"  # Default color        
    # Display the 'Medical Expertise' with conditional color highlighting
    st.markdown(f"""
        <ul>
            <li style="font-size:21px;"><strong>Medical Expertise:</strong> <span style="color:{color}; font-size:30px;">{me_judge}.</span>{me_reason}</li>
        </ul>
    """, unsafe_allow_html=True)
    
    fa_judge, par, fa_reason =  row['Facilities'].partition('.')
    if fa_judge.strip() == "Worse":
        color = "red"
    elif fa_judge.strip() == "Better":
        color = "green"
    else:
        color = "black"  # Default color                 
    # Display the 'Facilities' with conditional color highlighting and larger font size
    st.markdown(f"""
        <ul>
            <li style="font-size:21px;"><strong>Facilities:</strong> <span style="color:{color}; font-size:30px;">{fa_judge}.</span>{fa_reason}</li>
        </ul>
    """, unsafe_allow_html=True)

    
    sa_judge, par, sa_reason =  row['Service Attitude'].partition('.')
    if sa_judge.strip() == "Worse":
        color = "red"
    elif sa_judge.strip() == "Better":
        color = "green"
    else:
        color = "black"  # Default color        
    # Display the 'Service Attitude' with conditional color highlighting and larger font size
    st.markdown(f"""
        <ul>
            <li style="font-size:21px;"><strong>Service Attitude:</strong> <span style="color:{color}; font-size:30px;">{sa_judge}.</span>{sa_reason}</li>
        </ul>
    """, unsafe_allow_html=True)

    
    ca_judge, par, ca_reason =  row['Cost & Accessibility'].partition('.')
    if ca_judge.strip() == "Worse":
        color = "red"
    elif ca_judge.strip() == "Better":
        color = "green"
    else:
        color = "black"  # Default color           

    # Display the 'Cost & Accessibility' with conditional color highlighting and larger font size
    st.markdown(f"""
        <ul>
            <li style="font-size:21px;"><strong>Cost & Accessibility:</strong> <span style="color:{color}; font-size:30px;">{ca_judge}.</span>{ca_reason}</li>
        </ul>
    """, unsafe_allow_html=True)

          
    #st.markdown(f"- **Cost & Accessibility:** {ca_judge}. {ca_reason}")
else:
    st.error("The selected region does not exist in the data.")



st.markdown("---")  # Optional horizontal rule for separation
    

# AI Analysis
st.markdown("### Section V: Deep-dive into Alliance and competitor hospital branches with AI insights from reviews")
# st.markdown("#### User guide for this section:")
# st.markdown(
#     """
#     <div class="custom-font">
#     <ul>
#         <li><strong>Step 1 - Review Branches</strong>: Explore and locate branches of both companies based on specific criteria, including filtering by tiers, sorting by ratings in the table, and more.</li>
#         <li><strong>Step 2 - Select Companies</strong>: Choose either Alliance or the competitor.</li>       
#         <li><strong>Step 3 - Search Branches</strong>: Enter the name of the veterinary hospital branch you wish to investigate in the "Veterinary Hospital Branch Search" box. The search supports fuzzy matching, so entering just the first few words of the name is sufficient. You can then select the exact hospital name from the dropdown menu below the search box.</li>       
#         <li><strong>Step 4 - Get Insights Below</strong>:After selecting a branch, the AI analyzes all customer reviews and extracts key information, including common complaints, doctors linked to issues, recommendations, and praise for specific doctors, which is displayed at the bottom of the dashboard.</li>    </ul>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

st.markdown(
    """
    <div class="custom-font">
        In this section, you'll explore and analyze various hospital branches of Alliance Animal Health and its competitors. Leveraging AI-generated analyses of customer reviews, you'll gain valuable insights into branch performance, customer satisfaction, and areas for improvement. This process involves reviewing branch details, selecting specific companies, searching for particular branches, and accessing AI-extracted key findings to inform strategic decisions.
   </div>
    """,
    unsafe_allow_html=True
)
st.markdown("")
st.markdown(
    """
    <div class="custom-font">
        <strong>Step 1 - Review Branches</strong>: Explore and locate branches of both companies based on specific criteria, including filtering by tiers, sorting by ratings in the table, and more.
   </div>
    """,
    unsafe_allow_html=True
)

#%%Mannually change
aa_vvp_partners = pd.concat([aa_partners[['Company', 'Veterinary Partner Name', 'Location']], vvp_partners[['Company', 'Veterinary Partner Name', 'Location']]])
aa_vvp_partners['Hospital'] = aa_vvp_partners.apply(lambda x: x['Veterinary Partner Name'] +", " + x['Location'], axis=1) 
vet_reviews_details = pd.merge(vet_reviews_details, aa_vvp_partners[['Hospital', 'Company']], how="left", on="Hospital")
vet_reviews_details = vet_reviews_details.drop([106, 107], errors='ignore')

vet_reviews_details.loc[
    vet_reviews_details['Hospital'] == '30th Street Animal Hospital, Indianapolis, INDIANA',
    'Doctors Praised'
] = "Abby: identified as amazing, Dr. Barnes: praised for knowledge and explanatory skills, Dr. Sam: praised for diligently diagnosing and treating a dog's heart condition."


#%%
# Create Columns for Side-by-Side Layout
col5, col6 = st.columns(2)

tier_map = {"All":"All", 
            "Tier 1":"Top50% & AAHA Accredited",
            "Tier 2": "Top50% & Not AAHA Accredited",
            "Tier 3": "Bottom50% & AAHA Accredited",
            "Tier 4": "Bottom50% & Not AAHA Accredited"}


if not pd.isna(details_mapping):
    with col5: 
        # Left-Hand Side Box: Alliance Animal Health Practitioners
        st.markdown(
            f"<h3 style='color: orange;'>Alliance Animal Health - {total_practitioners_aa} Branches</h3>",
            unsafe_allow_html=True
        )
        # Ensure session state is initialized
        if "selected_category" not in st.session_state:
            st.session_state["selected_category"] = None
        # Simulate click interaction
        selected_category = st.selectbox(
            "Filter by Tiers to View Details:",
            options=["All",]+pie_data_aa["Category"], 
            key="category_selectbox"
        )
        # Update session state
        st.session_state["selected_category"] = selected_category
    
        # Display the corresponding table
        if (st.session_state["selected_category"]):
            category = st.session_state["selected_category"]
            st.write(f"Details for {category}:")
            df_aa = details_mapping[tier_map[category]].rename(columns={"Veterinary Partner Name":"Branch Name"})
            st.dataframe(df_aa.sort_values(by='Rating'))

if not pd.isna(details_mapping_comp):    
    with col6:  
        st.markdown(
            "<h3 style='color: purple;'>"+selected_option+ f" - {total_practitioners_comp} Branches</h3>",
            unsafe_allow_html=True
        )    
        # Ensure session state is initialized
        if "comp_selected_category" not in st.session_state:
            st.session_state["comp_selected_category"] = None
        # Simulate click interaction
        comp_selected_category = st.selectbox(
            "Filter by Tiers to View Details:",
            options=["All", "Tier 1", "Tier 2", "Tier 3", "Tier 4"],#["All",]+pie_data_comp["Category"],
            key="comp_category_selectbox"
        )
        # Update session state
        st.session_state["selected_category"] = comp_selected_category
    
        # Display the corresponding table
        if (st.session_state["selected_category"]):
            category = st.session_state["selected_category"]
            st.write(f"Details for {category}:")
            df_comp = details_mapping_comp[tier_map[category]].rename(columns={"Veterinary Partner Name":"Branch Name"})
            st.dataframe(df_comp.sort_values(by='Rating'))

# Example data
vet_reviews_details.rename(columns={"Hospital":"Branch Name"},inplace=True)
unique_companies = list(vet_reviews_details["Company"].unique())
# Create a selectbox for company selection
st.markdown(
    """
    <div class="custom-font">
        <strong>Step 2 - Choose either Alliance Animal Health or the competitor</strong>
   </div>
    """,
    unsafe_allow_html=True
)
selected_company = st.selectbox("For further deep-dive below", unique_companies)
vet_reviews_details = vet_reviews_details[vet_reviews_details["Company"]==selected_company]
# Search Functionality
#st.markdown("#### Veterinary Hospital Branch Search: Type the branch name for AI insights on customer reivews")
st.markdown(
    """
    <div class="custom-font">
        <strong>Step 3 - Hospital Branch Search</strong>: Type the branch name to receive AI-generated analyses of customer reviews.
   </div>
    """,
    unsafe_allow_html=True
)
# Auto-suggestion search box
search_input = st.text_input("Fuzzy-Search Branch Name", value="", placeholder="Start typing to search. Just the first few words of the name is sufficient...")

# Filter potential matches based on input
matching_names = vet_reviews_details[
    vet_reviews_details["Branch Name"].str.contains(search_input, case=False, na=False)
]["Branch Name"].tolist()

# Dropdown to select from matching results
#selected_name = st.selectbox("Select the exact hospital name from the dropdown menu", options=matching_names if matching_names else ["No matches found"])
# Define the default selection
default_selection = "Affordable Animal Hospital-Compton, Compton, CA"

# Sort the matching names alphabetically
matching_names = sorted(matching_names) if matching_names else []

# Check if the default selection is in the list of matching names
if default_selection in matching_names:
    selected_name = st.selectbox(
        "Select the exact hospital name that matches the fuzzy-search from the dropdown menu",
        options=matching_names if matching_names else ["No matches found"],
        index=matching_names.index(default_selection)
    )
else:
    selected_name = st.selectbox(
        "Select the exact hospital name from the dropdown menu",
        options=matching_names if matching_names else ["No matches found"]
    )



st.markdown(
    """
    <div class="custom-font">
        <strong>Step 4 - Access AI-Generated Insights</strong>: OpenAI has analyzed the branch's customer reviews to extract key findings.
   </div>
    """,
    unsafe_allow_html=True
)




# Display details as markdown when a selection is made
if selected_name and selected_name != "No matches found":
    #selected_details = vet_reviews_details[vet_reviews_details["Veterinary Partner Name"] == selected_name].iloc[0]
    selected_details = vet_reviews_details[vet_reviews_details["Branch Name"] == selected_name].iloc[0]
        
    # st.markdown(f"""
    #     <ul>
    #         <li><strong style="font-size:21px;">Key Complaints:</strong> <span style="font-size:21px;">{selected_details['Key Complaints']}</span></li>
    #         <li><strong style="font-size:21px;">Doctors with Complaints:</strong> <span style="font-size:21px;">{selected_details['Doctors with Complaints']}</span></li>
    #         <li><strong style="font-size:21px;">Key Recommendations:</strong> <span style="font-size:21px;">{selected_details['Key Recommendations']}</span></li>
    #         <li><strong style="font-size:21px;">Doctors Praised:</strong> <span style="font-size:21px;">{selected_details['Doctors Praised']}</span></li>
    #     </ul>
    # """, unsafe_allow_html=True)
    
    # Inject custom CSS to add indentation
    st.markdown(
        """
        <style>
        .indented-content {
            margin-left: 20px; /* Adjust the value as needed */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # st.markdown(
    #     f"""
    #     <div class="custom-font">
    #         <strong>For {selected_company}</strong>, below are key customer review AI insights of branch - <strong>{selected_details['Branch Name']}</strong>:
    #    </div>
    #     """,
    #     unsafe_allow_html=True
    # )
    # Display the indented list
    st.markdown(
        f"""
        <div class="indented-content">
            <strong style="font-size:21px;">For {selected_company}</strong><span style="font-size:21px;">, below are key customer review AI insights of branch - </span><strong style="font-size:21px;">{selected_details['Branch Name']}</strong>: 
            <ul>
                <li><strong style="font-size:21px;">Key Complaints:</strong> <span style="font-size:21px;">{selected_details['Key Complaints']}</span></li>
                <li><strong style="font-size:21px;">Doctors with Complaints:</strong> <span style="font-size:21px;">{selected_details['Doctors with Complaints']}</span></li>
                <li><strong style="font-size:21px;">Key Recommendations:</strong> <span style="font-size:21px;">{selected_details['Key Recommendations']}</span></li>
                <li><strong style="font-size:21px;">Doctors Praised:</strong> <span style="font-size:21px;">{selected_details['Doctors Praised']}</span></li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
        

