import pdfplumber
import pandas as pd

def extract_position_data(pdf_path, page_number, stat_labels, position_name): #Creates a function in order to pull data from position
    player_data = [] #Opens an empty data list

    with pdfplumber.open(pdf_path) as pdf: #Opens the pdf
        for page_num in page_number:
            page = pdf.pages[page_num]
            text = page.extract_text() #Extracts the text

            if text:
                lines = text.split('\n') #Splits the text
                for line in lines:
                    if "Projections" in line or "Team" in line:
                        continue
                    parts = line.split() #Splits the line
                    try:
                        for idx, token in enumerate(parts):
                            if token.replace('.', '', 1).isdigit(): #Looks for the first number
                                name_team = parts[:idx]
                                stats = parts[idx:]
                                break
                            else:
                                continue
                        
                        player_name = ' '.join(name_team[:-1]) #Joins the name and team
                        team = name_team[-1]
                        row = { #Creates a dictionary of the player's name and team
                            "Player": player_name,
                            "Team": team,
                            "Position": position_name.upper()
                        }
                        for j, label in enumerate(stat_labels): #Matches the stats to the labels
                            row[label] = stats[j] if j < len(stats) else None
                        player_data.append(row) 
                    except:
                        print("error", {line})
                        continue

    df = pd.DataFrame(player_data) #Creates a dataframe
    filename = f"{position_name.upper()}_Projections_2025.csv"
    df.to_csv(f'/Users/jaredmurray/Desktop/{filename}', index=False)
    print(f"Data saved to {filename}")
    return df

pdf_path = '/Users/jaredmurray/Downloads/NFL_Projections_2025.pdf'
qb_stat_labels = ["Rk", "FF Pts", "G Play", "Att", "Comp", "Pass Yds", "Pass TD", "INT", "Sk", "Carry", "Ru Yds", "Ru TD"]
qb_df = extract_position_data(pdf_path, [34], qb_stat_labels, "QB")

rb_stat_labels = ['Rk', 'FF Pts', 'G Play', 'Carry', 'Ry Yds', 'Ru TD', 'Targ', 'Rec', 'Re Yds', 'Re TD', 'Car%', 'Targ%']
rb_df = extract_position_data(pdf_path, [35, 36, 37] , rb_stat_labels, "RB")

wr_stat_labels = ['Rk', 'FF Pts', 'G Play', 'Carry', 'Ru Yds', 'Ru TD', 'Targ', 'Rec', 'Re Yds', 'Rec TD', 'Car%', 'Targ%']
wr_df = extract_position_data(pdf_path, [38, 39, 40, 41, 42], wr_stat_labels, "WR")

te_stat_labels = ['Rk', 'FF Pts', 'G Play', 'Carry', 'Ru Yds', 'Ru TD', 'Targ', 'Rec', 'Re Yds', 'Rec TD', 'Car%', 'Targ%']
te_df = extract_position_data(pdf_path, [43, 44], te_stat_labels, "TE")


    

