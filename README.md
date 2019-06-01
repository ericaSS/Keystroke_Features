# Keystroke_Features
 Keystroke Features: key hold and key interval Data Handling
**Abstract** <br/>
This program implemented the Manhattan verifier and computed the false accept (impostor pass) and 
false reject rates in terns of a publicly available keystroke dataset. Two features applied: key hold and 
key interval.  


**Author:** 
Shuxin Zhou

**Installing:**
pandas ,numpy libraries and function cityblock from scipy.spatial.distance

**Instruction:**<br/>
<body>
1. Download the dataset "DSL-StrongPasswordData.csv" and read in to the program; <br/>
2. Data splitted to two part, one is key hold, the other is key interval; <br/>
3. calculate the templates(mean) of each dataset in the function calculate_template(); <br/>
4. calculate the genuine and imposter scores of key hold data and key interval data, respectively
by using .cityblock built-in function of scipy library in the function calculate_manhattan_score(); <br/>
5. Based on the outcome of compute_manhattan_score, then calculte the false reject rate and imposter
pass rate of key hold and key interval features, seperately in the function compute_frr_ipr(); <br/>
6. run the program in the function run() with processing the data to genuine data and impostor data;
</body> 
