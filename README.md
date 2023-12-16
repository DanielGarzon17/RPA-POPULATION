Population Data Export
Considerations for this exercise:

- Use Selenium and Firefox
- Follow the steps exactly as the statement says
- Configure a local download folder in the code, the downloads that you want should be here.
- do the RPA.
- Use relative XPATH to find elements
- Use Try-Except-Raise
- Do not import libraries that are not used within the code or define variables that are not used
Step by Step
1. Go to the URL https://world-statistics.org/
2. Click on Indicators
3. Click on population
4. Click on Total Population
5. Click on Population, total (UN projection 1950 - 202 0)
6. Select the following countries and display them on the same sheet (Display All lines)
- Argentina
- Bolivia (Plurinational State of)
- Brazil
- Chili
- Colombia
- Ecuador
- Guyana
- Paraguay
- Peru
- Suriname
- Trinidad and Tobago
- Uruguay
- Venezuela (Bolivarian Republic of)

7. Export it in csv
8. We return to the indicators by clicking browse indicators
9. This time we choose Population, total (UN projection 2020-2100)
10. Select No change and choose the same countries
11. They download in CSV and this new download ignores (delete) the 2nd column.
12. The two downloaded files must be consolidated and at the end there must be a consolidated file
in csv as follows:

| Country | Year | Population
|---|---|---|
| Colombia | 1950 | 11981576
| Colombia | 1951 | 12295968
|... | ... | ...
