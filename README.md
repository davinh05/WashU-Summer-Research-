# WashU-Summer-Research-

**--- Overview ---**
Over the 2025 summer, I worked with the WashU Ashrafi Lab and received a summer stipend to complete my own project through the SURGE program which "provides stipends and flexible programming for WashU undergraduates pursuing faculty-mentored, project-based inquiry across all academic disciplines". I completed 10 weeks of research. 

This repository goes through much of the material that I contributed to throughout the course of my project, including data analysis pipelines (custom Python and Excel scripts that significantly sped up data analysis), a poster that I created to synthesize my research, and a lab presentation I gave to my lab. 

The rest of the text in this READme file is meant to give a broad overview of the project, where much of this information will be further explored in additional documents in this repository. 

**--- Research Overview and Significance ---**
The goal of this summer project is to study how neurons utilize alternative energy sources when access to glucose becomes limiting, such as during stroke, starvation, or other forms of metabolic stress. Among these alternative fuels are ketone bodies, which are supplied to neurons through the circulation or by neighboring glial cells. Ketogenic diets, which are high-fat low carbohydrate-diets, have been used for decades as an effective treatment for drug-resistant childhood epilepsies (Dy ´nka, Kowalcze, and Paziewska 2022). More recently, these diets have been explored to improve cognitive function in neurodegenerative diseases like Alzheimer's and Parkinson's (Yang et al. 2019). Nevertheless, neuronal mechanisms of ketone metabolism and their impact on the brain remain poorly understood.

**--- Methodology ---**
Overview: Primary cultures of hippocampal neurons (14–17 days in vitro) are prepared from neonatal rats. Hippocampal neurons are used for live-imaging and functional assays. Cultures are kept at 37 ºC and 5% CO2 and in 25mM glucose and transferred to media containing 5mM glucose or BHB. These settings attempt to model neuron settings in the body under normal circumstances and with ketones used as the primary source of energy (with the ketogenic diet). Live imaging is performed on 10–15 individual neurons from 5–7 independent neuronal cultures, supplied with different fuel types as described in aim 1. Neurons are transfected with the appropriate optical sensors and images will be collected with a sensitive EMCCD camera on a custom microscope setup. Neurotransmitter release is monitored with the glutamate sensor iGluSnFR3. Image analysis is performed using existing pipelines in the lab, such as, Image J plugins, and a custom-built semi-automated analysis code for ATP measurements (Dehkharghanian, Hashemiaghdam, and Ashrafi 2022). Python code is used to automate much of this analysis, making analysis on large data sets possible.

Wet-lab (overall goal to collect hippocampal neuron data): 
  • Transfect hippocampal cells from prenatal rat pups with edited iGluSnFR3 plasmids (lab manager completed this step)
  • CRISPR/CAS9 edits genome to add fluorescent tags to neurons
  • Neurons are seperated into two seperate cultures of glucose and BHB
  • Neurons are stimulated at 1HZ and 20HZ for each media condition
  • Images are captured under EMCCD microscopy
  
Dry-lab (overall goal to analyze the collected data):
  • Images are converted to ImageJ where fluorescence can be quanitified
  
   - I TALK MORE ABOUT THIS IN THE MY CONTRIBUTION SECTION, BUT THIS IS WHERE I HAD FIGURED OUT A MORE OPTIMAL WAY TO ANALYZE THE DATA AND CREATED MY OWN PYTHON/EXCEL SCRIPTS -
     
  • Fluorescense data is pasted into an initial Excel file to organize data. The data in this file is normalized and set up so a custom python script can read the data.
  • Python reads, analyzes, and outputs data to a secondary Excel file. In addition, the python code included functions to test and visualize the data to ensure that the data was being properly processed.           Fluorsecent peaks are automatically found for the 1HZ data and sent to the second Excel File.
  • GraphPad Prism is used to find the rate of decay for the 20Hz data, and this value is pasted manually into the second Excel file
  • A second Excel file is where the python data is sent to. The data is automatically combined from multiple neurons to compile an averaged data set with visualized data to easily deliver to lab mentor and         principle investigator.
  • AT THE VERY END OF THE SUMMER, once all of the data sets were collected, a complete, averaged data set was created to completly synthesize findings

**--- My Contribution ---**
While I completed both the wet-lab and dry-lab components of the project, the biggest impact that I had was creating a much faster pipleine to analyze data. The wet-lab portion of the lab was very established, however, the data analysis pipeline was not very established. After collecting the data from the neurons, a very large dataset was created that at the time took over eight hours to analyze. I brought that analysis time down to two hours. I was also able to generate preliminary trends which have given insights to drive future directions for the project. 

**--- Key Findings ---**
Preliminary trends observed were that neurons in the BHB media fired less intensely than those in the glucose media when stimulated at 20HZ (AP train). In addition, the rate of decay for neurons stimulated with the AP train in BHB was smaller than that of glucose. However, when analyzing the neurons that were stimulated at 1HZ, there appeared to be no significant difference in the neuronal activity between the hippocampal cells in BHB and in glucose.

These preliminary trends allow us to focus more on how higher frequency stimulations.

It is very important to note that all preliminary findings are NOT significant due to a high level of variance between each data set. However, within each data set the same trends appeared but when we combined the normalized data across data sets, there was a high level of variance in the magnitude of fluorescence. Therefore, throughout much of this project preliminary findings are often labeled as "preliminary trends" instead. 
