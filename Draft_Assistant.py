import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# --- Loaded CSV files ---
qb_df = pd.read_csv('/Users/jaredmurray/Desktop/QB_Projections_2025.csv') #Reads QB data
rb_df = pd.read_csv('/Users/jaredmurray/Desktop/RB_Projections_2025.csv') #Reads RB data
wr_df = pd.read_csv('/Users/jaredmurray/Desktop/WR_Projections_2025.csv') #Reads WR data
te_df = pd.read_csv('/Users/jaredmurray/Desktop/TE_Projections_2025.csv') #Reads TE data

all_players_df = pd.concat([qb_df, rb_df, wr_df, te_df], ignore_index=True) #Combines the data, just incase we need a mother document

all_players_df.to_csv('/Users/jaredmurray/Desktop/All_Players_Projections_2025.csv', index=False) #Saves a CSV of all data combined

drafted_players = set()

def mark_drafted_players(player_name, drafted_set):
    drafted_players.add(player_name.lower())
    print(f">>> {player_name} has been drafted!\n <<<")

def plot_sleepers(df, position_name, drafted_set, top_n = 10, Rk_cutoff = 20):
    df = df.copy()
    df["Rk"] = pd.to_numeric(df['Rk'], errors='coerce')
    df["FF Pts"] = pd.to_numeric(df["FF Pts"], errors='coerce')
    df = df.dropna(subset=['Rk', 'FF Pts']) #Removes any data with missing values
    df = df[~df['Player'].str.lower().isin({name.lower() for name in drafted_players})] #Removes any drafted player
    df['Value Score'] = df['FF Pts'] / df['Rk'] #Creates an equation for value score
    sleepers = df[df['Rk'] > Rk_cutoff] #Removes any player with a rank lower than 20
    top_sleepers = sleepers.sort_values(by='Value Score', ascending=False).head(top_n) #Sorts the data by value score and takes the top n amount

    if top_sleepers.empty:
        print(f"There are no sleepers for {position_name}!\n")
        return
    #plot the chart
    plt.figure(figsize = (10, 6))
    sns.barplot(
        data = top_sleepers,
        x = 'Value Score',
        y = 'Player',
        palette = 'colorblind'
    )
    plt.title(f'Top{top_n} sleepers for {position_name.upper()} - Undrafted')
    plt.xlabel('Value Score')
    plt.ylabel(top_sleepers['Player'] + " (" + top_sleepers['Position'] + ")")
    plt.tight_layout()
    plt.show()

def draft_assistant():
    print("Welcome to the Draft Assistant (Sleepers Finder")
    print("------------------------------------------")

    while True:
        position = input("Enter the position you are drafting (QB, RB, WR, TE, ALL) or 'exit': ").upper()
        if position == 'EXIT':
            break
        elif position not in ['QB', 'RB', 'WR', 'TE', 'ALL']: 
            print("Invalid position. Please enter a valid position (QB, RB, WR, TE).\n")
            continue

        if position == 'RB':
            df = rb_df
        if position == 'WR':
            df = wr_df
        if position == 'TE':
            df = te_df
        if position == 'QB':
            df = qb_df
        if position == 'ALL':
            df = all_players_df

        draft = input("Enter name of player drafted or enter 'show' to see sleepers: ").lower()

        if draft == 'show':
            try:
                top_n = int(input("How many sleepers would you like to see? "))
                Rk_cutoff = int(input("Exlcude players that are ranked higher than what number? :"))
            except ValueError:
                print("Input error. Showing default values (Top 10 sleepers, Rk < 20).\n")
                top_n = 10
                Rk_cutoff = 20
            plot_sleepers(df, position, drafted_players, top_n=top_n, Rk_cutoff=Rk_cutoff)
        else:
            mark_drafted_players(draft, drafted_players)

if __name__ == '__main__':
    draft_assistant()
    




