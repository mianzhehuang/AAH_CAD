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
    page_title="Alliance Animal Health Competitor Analysis",
    layout="wide",  # Makes the dashboard use the full width of the screen
    initial_sidebar_state="expanded"  # Expands the sidebar by default
)

# Title for the dashboard
st.title("Alliance Animal Health Competitor Analysis")

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
    f"{name} (Data Unavailable)" if not available else name
    for name, available in options.items()
]

# Create the selectbox with all options
selected_display_option = st.sidebar.selectbox("Select Competitor", display_options)

# Map the selected display option back to the original option name
selected_option = selected_display_option.replace(" (Data Unavailable)", "")

# Check if the selected option has data available
if options[selected_option]:
    st.write(f"Displaying data for {selected_option}")
else:
    st.warning(f"Data for {selected_option} is currently unavailable.")
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
    title={
        "text": "US Veterinary Practitioners Presence based on Population Density",
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


# Create Columns for Side-by-Side Layout
st.markdown("---")  # Optional horizontal rule for separation
col1, col2 = st.columns(2)

with col1:
    # Left-Hand Side Box: Alliance Animal Health Practitioners
    st.markdown(
        "<h2 style='color: orange;'>Alliance Animal Health</h2>",
        unsafe_allow_html=True
    )
    
with col2:
    st.markdown(
        "<h2 style='color: purple;'>"+selected_option+"</h2>",
        unsafe_allow_html=True
    )    
    
# 1. # Total Practitioners
total_practitioners_aa = int(vets_sum.loc[
    vets_sum["Region"] == selected_region, "Veterinary Partner Name"
].values[0])

# 2. Overall Rating / Total Reviews
rating_aa = vets_sum.loc[vets_sum["Region"] == selected_region, "Rating"].values[0]
total_reviews_aa = vets_sum.loc[
    vets_sum["Region"] == selected_region, "Total Ratings #"
].values[0]

# Format total_reviews_aa with commas
total_reviews_aa_formatted = f"{int(total_reviews_aa):,}"
with col1:
    # Display the Information
    st.markdown(f"### Total Practitioners #: {total_practitioners_aa}")
    st.markdown(
        f"### Rating / Reviews: {rating_aa:.2f} / {total_reviews_aa_formatted}"
    )


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
            "Top50% & AAHA Accredited",
            "Top50% & Not AAHA Accredited",
            "Bottom50% & AAHA Accredited",
            "Bottom50% & Not AAHA Accredited",
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
    with col1:
        #st.subheader("Alliance Animal Health Practitioner Ratings")
        # Create the pie chart with explicit category order
        pie_fig_aa = px.pie(
            pie_data_aa,
            names="Category",
            values="Count",
            color="Category",
            color_discrete_map={
                "Top50% & AAHA Accredited": "darkblue",
                "Top50% & Not AAHA Accredited": "blue",
                "Bottom50% & AAHA Accredited": "lightblue",
                "Bottom50% & Not AAHA Accredited": "white",
            },
            title="Ratings & Accreditation Breakdown",
            category_orders={
                "Category": [
                    "Top50% & AAHA Accredited",
                    "Top50% & Not AAHA Accredited",
                    "Bottom50% & AAHA Accredited",
                    "Bottom50% & Not AAHA Accredited",
                ]
            },
        )
        st.plotly_chart(pie_fig_aa, use_container_width=True)
else:
    details_mapping = np.nan



        
# 1. # Total Practitioners
total_practitioners_comp = comp_vets_sum.loc[
    comp_vets_sum["Region"] == selected_region, "Veterinary Partner Name"
].values[0]

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
    st.markdown(f"### {total_practitioners_comp}")
    st.markdown(
        f"### {rating_comp:.2f} / {total_reviews_comp_formatted}"
    )

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
            "Top50% & AAHA Accredited",
            "Top50% & Not AAHA Accredited",
            "Bottom50% & AAHA Accredited",
            "Bottom50% & Not AAHA Accredited",
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
    
    with col2:
        # Create the pie chart with explicit category order
        pie_fig_comp = px.pie(
            pie_data_comp,
            names="Category",
            values="Count",
            color="Category",
            color_discrete_map={
                "Top50% & AAHA Accredited": "darkblue",
                "Top50% & Not AAHA Accredited": "blue",
                "Bottom50% & AAHA Accredited": "lightblue",
                "Bottom50% & Not AAHA Accredited": "white",
            },
            title="Ratings & Accreditation Breakdown",
            category_orders={
                "Category": [
                    "Top50% & AAHA Accredited",
                    "Top50% & Not AAHA Accredited",
                    "Bottom50% & AAHA Accredited",
                    "Bottom50% & Not AAHA Accredited",
                ]
            },
        )
        # Hide the legend
        pie_fig_comp.update_layout(showlegend=False)
        st.plotly_chart(pie_fig_comp, use_container_width=True)
else:
    details_mapping_comp = np.nan


vets_reviews_region_sum = pd.read_pickle(r"vets_reviews_region_sum.pkl")
filtered_df = vets_reviews_region_sum[vets_reviews_region_sum['Region']==selected_region]

# Check if the region exists in the DataFrame
if not filtered_df.empty:
    # Extract the row corresponding to the selected region
    row = filtered_df.iloc[0]
    
    # Display the details using markdown
    st.markdown(f"### Based on customer reviews, is Alliance Animal Health better or worse than {selected_option}?")
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


st.markdown("**Reference:** [AAHA (American Animal Hospital Association) Accreditation.](https://www.aaha.org/for-pet-parents/find-an-aaha-hospital/) The only organization that accredits veterinary practices in the US and CA based on rigorous quality standards")

st.markdown("---")  # Optional horizontal rule for separation
    

# Create Columns for Side-by-Side Layout
col3, col4 = st.columns(2)



if not pd.isna(details_mapping):
    with col3:    
        # Ensure session state is initialized
        if "selected_category" not in st.session_state:
            st.session_state["selected_category"] = None
        # Simulate click interaction
        selected_category = st.selectbox(
            "Select a Category to View Details:",
            options=["All",]+pie_data_aa["Category"], 
            key="category_selectbox"
        )
        # Update session state
        st.session_state["selected_category"] = selected_category
    
        # Display the corresponding table
        if (st.session_state["selected_category"]):
            category = st.session_state["selected_category"]
            st.write(f"Details for {category}:")
            df_aa = details_mapping[category]
            st.dataframe(df_aa)

if not pd.isna(details_mapping_comp):    
    with col4:  
        # Ensure session state is initialized
        if "comp_selected_category" not in st.session_state:
            st.session_state["comp_selected_category"] = None
        # Simulate click interaction
        comp_selected_category = st.selectbox(
            "Select a Category to View Details:",
            options=["All",]+pie_data_comp["Category"],
            key="comp_category_selectbox"
        )
        # Update session state
        st.session_state["selected_category"] = comp_selected_category
    
        # Display the corresponding table
        if (st.session_state["selected_category"]):
            category = st.session_state["selected_category"]
            st.write(f"Details for {category}:")
            st.dataframe(details_mapping_comp[category])

# Example data
vet_reviews_details.rename(columns={"Hospital":"Veterinary Partner Name"},inplace=True)
# Search Functionality
st.header("Veterinary Partner Search")

# Auto-suggestion search box
search_input = st.text_input("Search Veterinary Partner Name", value="", placeholder="Start typing to search...")

# Filter potential matches based on input
matching_names = vet_reviews_details[
    vet_reviews_details["Veterinary Partner Name"].str.contains(search_input, case=False, na=False)
]["Veterinary Partner Name"].tolist()

# Dropdown to select from matching results
selected_name = st.selectbox("Select a Veterinary Partner", options=matching_names if matching_names else ["No matches found"])

# Display details as markdown when a selection is made
if selected_name and selected_name != "No matches found":
    selected_details = vet_reviews_details[vet_reviews_details["Veterinary Partner Name"] == selected_name].iloc[0]
    st.markdown(f"""
        ### Details for {selected_details['Veterinary Partner Name']}
        <ul>
            <li><strong style="font-size:21px;">Key Complaints:</strong> <span style="font-size:21px;">{selected_details['Key Complaints']}</span></li>
            <li><strong style="font-size:21px;">Doctors with Complaints:</strong> <span style="font-size:21px;">{selected_details['Doctors with Complaints']}</span></li>
            <li><strong style="font-size:21px;">Key Recommendations:</strong> <span style="font-size:21px;">{selected_details['Key Recommendations']}</span></li>
            <li><strong style="font-size:21px;">Doctors Praised:</strong> <span style="font-size:21px;">{selected_details['Doctors Praised']}</span></li>
        </ul>
    """, unsafe_allow_html=True)


        



