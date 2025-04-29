# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Accommodation Dashboard", layout="wide")

# Load data
def load_data():
    file_path = "https://raw.githubusercontent.com/FrankPerera04/DSPL_Individual_CW/refs/heads/main/processed_accommodation_data%20(1).csv"
    df = pd.read_csv(file_path)
    return df

df = load_data()

# Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Go to",
    ("About",
     "Accommodation Capacity by Region",
     "Type Distribution",
     "Quality of Accommodation",
     "Geographic Gaps",
     "Action Signals")
)

# Sidebar Filters
st.sidebar.header("🔎 Filter Options")

# District filter (multi-select)
all_districts = sorted(df["District"].dropna().unique().tolist())
selected_districts = st.sidebar.multiselect("Select District(s)", options=["All"] + all_districts, default=["All"])

# Accommodation Type filter (multi-select)
all_types = sorted(df["Type"].dropna().unique().tolist())
selected_types = st.sidebar.multiselect("Select Accommodation Type(s)", options=["All"] + all_types, default=["All"])

# Apply filters
filtered_df = df.copy()
if "All" not in selected_districts:
    filtered_df = filtered_df[filtered_df["District"].isin(selected_districts)]
if "All" not in selected_types:
    filtered_df = filtered_df[filtered_df["Type"].isin(selected_types)]

# Main Page Routing
if page == "About":
    bg_image_url = "https://raw.githubusercontent.com/FrankPerera04/DSPL_Individual_CW/main/Images/About.jpeg"

     # Add background and dark overlay
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: linear-gradient(
                 rgba(0, 0, 0, 0.7),
                 rgba(0, 0, 0, 0.7)
             ), url("{bg_image_url}");
             background-size: cover;
             background-position: center;
             background-repeat: no-repeat;
             background-attachment: fixed;
             color: white;
         }}
         .block-container {{
             background-color: rgba(0, 0, 0, 0);
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

    # About Page Content
    st.markdown("""
    # Accomodation Insights
    ---
    ### Purpose
    This dashboard provides key insights into accommodation trends across **Sri Lanka**.
    It is designed to help **government officials** make informed decisions regarding tourism development, infrastructure investment, and policy planning.

    ### Focus Areas
    - Accommodation Capacity Analysis
    - Popular Accommodation Types
    - Quality of Accommodation
    - Gap and Weak Points Identification
    - Possible Improvements


    ### Key Features
    - Accommodation Capacity
    - Room availability across the island
    - Breakdown of the most common accommodation types
    - Gap and weak points analysis
    - Provincial and city-level comparisons


    ### Intended Users
    - Government officials
    - Policymakers
    - Tourism and regional development stakeholders


    ### Data Sources
    - Open Data Portal of Sri Lanka
    - Tourism and Leisure
    - Accommodation Information for Tourists

    ### Disclaimer
    The information provided in this dashboard is for informational purposes only.
    Even though efforts have been made to ensure the accuracy of the data, users are advised to independently verify information before decision making.

    ---
    """)


elif page == "Accommodation Capacity by Region":
    st.title("Accommodation Capacity by Region")

    # Total number of accommodations per district
    st.subheader("Total Number of Accommodations per District")
    accommodations_per_district = filtered_df.groupby("District")["Name"].count().reset_index().sort_values(by="Name", ascending=False)
    fig1 = px.bar(accommodations_per_district, x="District", y="Name", color="Name", text="Name", template="plotly_dark")
    fig1.update_layout(xaxis_title="District", yaxis_title="Total Accommodations", xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)

    # Total number of rooms per district
    st.subheader("Total Number of Rooms per District")
    rooms_per_district = filtered_df.groupby("District")["Rooms"].sum().reset_index().sort_values(by="Rooms", ascending=False)
    fig2 = px.bar(rooms_per_district, x="District", y="Rooms", color="Rooms", text="Rooms", template="plotly_dark")
    fig2.update_layout(xaxis_title="District", yaxis_title="Total Rooms", xaxis_tickangle=-45)
    st.plotly_chart(fig2, use_container_width=True)

    # Average size of accommodations
    st.subheader("Average Size of Accommodations (Rooms per Property)")
    avg_rooms_per_property = (filtered_df.groupby("District")["Rooms"].mean()).reset_index().sort_values(by="Rooms", ascending=False)
    fig3 = px.bar(avg_rooms_per_property, x="District", y="Rooms", color="Rooms", text=avg_rooms_per_property["Rooms"].round(1), template="plotly_dark")
    fig3.update_layout(xaxis_title="District", yaxis_title="Average Rooms per Property", xaxis_tickangle=-45)
    st.plotly_chart(fig3, use_container_width=True)


elif page == "Type Distribution":
    st.title("Accommodation Type Distribution")

    type_distribution = filtered_df["Type"].value_counts().reset_index()
    type_distribution.columns = ["Accommodation Type", "Count"]

    fig_type = px.pie(
        type_distribution,
        names="Accommodation Type",
        values="Count",
        title="Accommodation Types Share",
        hole=0.4,
        template="plotly_dark"
    )
    st.plotly_chart(fig_type, use_container_width=True)

    st.dataframe(type_distribution, use_container_width=True)


elif page == "Quality of Accommodation":
    st.title("Quality of Accommodation (Based on Grades)")

    # Filter out rows where Grade is not null
    grade_df = filtered_df[filtered_df["Grade"].notna() & (filtered_df["Grade"].str.strip().str.lower() != "null")]

    if not grade_df.empty:
        # Bar Chart: Number of accommodations per Grade
        st.subheader("📈 Number of Accommodations by Grade")
        grade_counts = grade_df["Grade"].value_counts().reset_index()
        grade_counts.columns = ["Grade", "Count"]

        fig_grade_bar = px.bar(
            grade_counts,
            x="Grade",
            y="Count",
            color="Count",
            text="Count",
            title="Number of Accommodations by Grade",
            template="plotly_dark"
        )
        fig_grade_bar.update_layout(xaxis_title="Grade", yaxis_title="Number of Accommodations")
        st.plotly_chart(fig_grade_bar, use_container_width=True)

        # Pie Chart: Share of each Grade
        st.subheader("🧩 Accommodation Grade Distribution")
        fig_grade_pie = px.pie(
            grade_counts,
            names="Grade",
            values="Count",
            title="Accommodation Grade Share",
            hole=0.4,
            template="plotly_dark"
        )
        st.plotly_chart(fig_grade_pie, use_container_width=True)


        # Grade distribution across Accommodation Types
        st.subheader("📊 Grade Distribution by Accommodation Type")
        type_grade_df = grade_df.groupby(["Type", "Grade"]).size().reset_index(name="Count")

        fig_type_grade = px.bar(
            type_grade_df,
            x="Type",
            y="Count",
            color="Grade",
            title="Accommodation Grade Breakdown by Type",
            template="plotly_dark",
            barmode="stack"
        )
        fig_type_grade.update_layout(xaxis_title="Accommodation Type", yaxis_title="Number of Accommodations")
        st.plotly_chart(fig_type_grade, use_container_width=True)

        # Data Table for Type and Grade
        st.dataframe(type_grade_df, use_container_width=True)

    else:
        st.info("ℹ️ No grade information available for the selected filters.")



elif page == "Geographic Gaps":
    st.title("Geographic Gaps")

    district_counts = filtered_df.groupby("District").agg(Total_Accommodations=("Name", "count")).reset_index()
    map_df = pd.merge(filtered_df, district_counts, on="District", how="left")

    st.map(map_df[["Latitude", "Logitiute"]].rename(columns={"Logitiute": "longitude", "Latitude": "latitude"}))

    low_accommodation_threshold = 5
    low_acc_districts = district_counts[district_counts["Total_Accommodations"] <= low_accommodation_threshold]

    if not low_acc_districts.empty:
        st.warning("⚠️ Districts with very few accommodations (<= 5):")
        st.dataframe(low_acc_districts, use_container_width=True)
    else:
        st.success("✅ All districts have sufficient accommodation coverage.")



elif page == "Action Signals":
    st.title("Action Signals: Target for Improvements")

    low_threshold = 5
    action_df = filtered_df.groupby("District").agg(
        Total_Accommodations=("Name", "count"),
        Total_Rooms=("Rooms", "sum")
    ).reset_index()

    low_accommodation_districts = action_df[action_df["Total_Accommodations"] <= low_threshold]

    if not low_accommodation_districts.empty:
        st.warning(f"⚠️ {len(low_accommodation_districts)} District(s) have <= {low_threshold} accommodations. Consider investing here!")
        st.dataframe(low_accommodation_districts, use_container_width=True)

        fig_low = px.bar(
            low_accommodation_districts,
            x="District",
            y="Total_Accommodations",
            color="Total_Accommodations",
            text="Total_Accommodations",
            title="Districts with Low Number of Accommodations",
            template="plotly_dark"
        )
        fig_low.update_layout(xaxis_title="District", yaxis_title="Total Accommodations", xaxis_tickangle=-45)
        st.plotly_chart(fig_low, use_container_width=True)
    else:
        st.success("All districts have sufficient number of accommodations!")
