import pandas as pd

with open('debug_output.txt', 'w') as f:
    opg_df = pd.read_csv('OPGRegionData.csv')
    f.write('OPG columns: ' + str(opg_df.columns.tolist()) + '\n')
    f.write('OPG first row:\n')
    f.write(str(opg_df.iloc[0]) + '\n\n')

    ic3_df = pd.read_csv('IC3RegionData.csv')
    f.write('IC3 columns: ' + str(ic3_df.columns.tolist()) + '\n')
    f.write('IC3 first row:\n')
    f.write(str(ic3_df.iloc[0]) + '\n')

