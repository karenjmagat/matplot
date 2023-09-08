#!/usr/bin/env python
# coding: utf-8

# # Pymaceuticals Inc.
# ---
# 
# ### Analysis
# 
# - Add your analysis here.
#  

# In[1]:


# dependencies
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st

#data files
mouse_metadata_path = "./data/Mouse_metadata.csv"
study_results_path = "./data/Study_results.csv"

# Read data
mouse_metadata = pd.read_csv(mouse_metadata_path)
study_results = pd.read_csv(study_results_path)

# Combine the data into a single DataFrame
study_complete_df = pd.merge(study_results, mouse_metadata, how="left",on="Mouse ID")

# Display the data table for preview
study_complete_df


# In[2]:


# 2. Display number of unique mice IDs
len(study_complete_df["Mouse ID"].unique())


# In[3]:


#Check for any mouse ID with duplicate time points
# Get the duplicate mice by ID number that shows up for Mouse ID and Timepoint. 
duplicate_mouse_id = study_complete_df[study_complete_df.duplicated(subset=["Mouse ID","Timepoint"])]["Mouse ID"].unique()
duplicate_mouse_id 


# In[4]:


#Display data associated with that mouse ID
duplicated_mouse_data =study_complete_df[study_complete_df["Mouse ID"] == "g989"]
duplicated_mouse_data


# In[5]:


#Clean data - filter out duplicates
clean_data = study_complete_df[study_complete_df["Mouse ID"].isin(duplicate_mouse_id) == False]
clean_data


# In[6]:


#Updated number of unique mice IDs
len(clean_data["Mouse ID"].unique())


# ## Summary Statistics

# In[7]:


#Create a DataFrame of summary statistics. Remember, there is more than one method to produce the results you're after, so the method you use is less important than the result.
#Your summary statistics should include:
#A row for each drug regimen. These regimen names should be contained in the index column.
#A column for each of the following statistics: mean, median, variance, standard deviation, and SEM of the tumor volume.

mean = clean_data.groupby("Drug Regimen").mean()["Tumor Volume (mm3)"]
median = clean_data.groupby("Drug Regimen").median()["Tumor Volume (mm3)"]
variance = clean_data.groupby("Drug Regimen").var()["Tumor Volume (mm3)"]
standard_deviation = clean_data.groupby("Drug Regimen").std()["Tumor Volume (mm3)"]
sems = clean_data.groupby("Drug Regimen").sem()["Tumor Volume (mm3)"]

summary_statistics_table = pd.DataFrame({
    "Mean Tumor Volume": mean,
    "Median Tumor Volume": median,
    "Tumor Volume Variance": variance,
    "Tumor Volume Std. Dev": standard_deviation,
    "Tumor Colume Std. Err": sems
    
    
}
)
summary_statistics_table


# ## Bar and Pie Charts

# In[8]:


#Generate two bar charts. Both charts should be identical and show the total total number of rows (Mouse ID/Timepoints) for each drug regimen throughout the study.
#Create the first bar chart with the Pandas DataFrame.plot() method.

count = clean_data["Drug Regimen"].value_counts()
count.plot(kind= "bar", color = "purple", alpha = .5)
plt.xlabel("Drug Regimen")
plt.xticks(rotation = 75)
plt.ylabel("# of Mice Tested")
plt.show()


# In[9]:


# Generate a bar plot showing the total number of rows (Mouse ID/Timepoints) for each drug regimen using pyplot.
#Create the second bar chart with Matplotlib's pyplot methods.
counts = clean_data["Drug Regimen"].value_counts()
plt.bar(counts.index.values, counts.values,color = "pink", alpha = .5)
plt.xlabel("Drug Regimen")
plt.xticks(rotation = 75)
plt.ylabel("# of Mice Tested")
plt.show()


# In[10]:


#Generate two pie charts. Both charts should be identical and show the distribution of female versus male mice in the study.

#Create the first pie chart with the Pandas DataFrame.plot() method.
counts = clean_data.Sex.value_counts()


counts.plot(kind = "pie", autopct ="%1.1f%%",colors = ["red","pink"], shadow = True)
plt.show()


# In[11]:


#Create the second pie chart with Matplotlib's pyplot methods.
counts = clean_data.Sex.value_counts()
plt.pie(counts.values, labels = counts.index.values, autopct ="%1.1f%%",colors = ["red","pink"])
plt.ylabel =("Sex")
plt.show()


# ## Quartiles, Outliers and Boxplots

# In[12]:


# Calculate the final tumor volume of each mouse across four of the treatment regimens:  
# Capomulin, Ramicane, Infubinol, and Ceftamin

#Create a grouped DataFrame that shows the last (greatest) time point for each mouse. Merge this grouped DataFrame with the original cleaned DataFrame.
max_tumor = clean_data.groupby(["Mouse ID"])["Timepoint"].max()
max_tumor = max_tumor.reset_index()

merged_data = max_tumor.merge(clean_data, on=["Mouse ID","Timepoint"], how = "left")


# In[13]:


#Create a list that holds the treatment names Capomulin, Ramicane, Infubinol, and Ceftaminas well as a second, empty list to hold the tumor volume data.
#Loop through each drug in the treatment list, locating the rows in the merged DataFrame that correspond to each treatment. Append the resulting final tumor volumes for each drug to the empty list.
#Determine outliers by using the upper and lower bounds, and then print the results.
treatment_name = ["Capomulin", "Ramicane", "Infubinol","Ceftamin"]

tumor_volume_list =[]

for drug in treatment_name:
    final_tumor_volume = merged_data.loc[merged_data["Drug Regimen"]== drug, "Tumor Volume (mm3)"]
    tumor_volume_list.append(final_tumor_volume)
    
    quartiles = final_tumor_volume.quantile([.25,.5,.75])
    lower_quartiles = quartiles [0.25]
    upper_quartiles = quartiles[0.75]
    iqr = upper_quartiles-lower_quartiles
    lower_bound = lower_quartiles - (1.5 * iqr)
    upper_bound = upper_quartiles + (1.5 * iqr)
    
    outliers = final_tumor_volume.loc[(final_tumor_volume < lower_bound) | (final_tumor_volume > upper_bound)]
    print(f"{drug}'s potential outliers {outliers} ")


# In[14]:


# Using Matplotlib, generate a box plot that shows the distribution of the final tumor volume for all the mice in each treatment group. Highlight any potential outliers in the plot by changing their color and style.
box_out = dict(markerfacecolor = 'red' , markersize=10)
plt.boxplot(tumor_volume_list, labels = treatment_name, flierprops = box_out)
plt.ylabel("Tumor Volume (mm3)")
plt.show()


# ## Line and Scatter Plots

# In[15]:


#Select a single mouse that was treated with Capomulin, and generate a line plot of tumor volume versus time point for that mouse.

capomulin_data = clean_data[clean_data["Drug Regimen"] == "Capomulin"]
mouse_data = capomulin_data[capomulin_data["Mouse ID"] == "s185"]
mouse_data
plt.plot(mouse_data["Timepoint"], mouse_data["Tumor Volume (mm3)"], color='skyblue', alpha=0.3)
plt.xlabel("Timepoint in Days")
plt.ylabel("Tumor Volume (mm3)")
plt.title("Capomulin Treatment")
plt.show()


# In[17]:


# Generate a scatter plot of mouse weight versus average observed tumor volume for the entire Capomulin treatment regimen.
capomulin_table = clean_data[clean_data["Drug Regimen"] == "Capomulin"]
capomulin_avg = capomulin_table.groupby(["Mouse ID"]).mean()
plt.scatter(capomulin_avg["Weight (g)"], capomulin_avg["Tumor Volume (mm3)"])
plt.xlabel("Weight")
plt.ylabel("Avg Tumor Volume")
plt.show()


# ## Correlation and Regression

# In[32]:


#Calculate the correlation coefficient and linear regression model between mouse weight and average observed tumor volume for the entire Capomulin treatment regimen.
#Plot the linear regression model on top of the previous scatter plot.

correlation = st.pearsonr(capomulin_avg["Weight (g)"], capomulin_avg["Tumor Volume (mm3)"])
print(f" The correlation between mouse weight and the average tumor volume is {round(correlation[0],2)}")

model = st.linregress(capomulin_avg["Weight (g)"], capomulin_avg["Tumor Volume (mm3)"])
slope = model[0]
b = model[1]
y_values = capomulin_avg["Weight (g)"] * slope + b
plt.scatter(capomulin_avg["Weight (g)"], capomulin_avg["Tumor Volume (mm3)"])
plt.plot(capomulin_avg["Weight (g)"], y_values, color = "red")
plt.xlabel("Weight")
plt.ylabel("Avg Tumor Volume")
plt.show


# In[ ]:




