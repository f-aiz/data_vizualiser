import pandas as pd
import numpy as np
import mysql.connector as c
import plotly.graph_objects as go
import plotly.io as pio

df = pd.DataFrame()
x = ""
y = ""
z = ""

def collection():
    global df  # Declare df as global
    typ = input("Select document type \n 1. Excel \n 2. Csv \n 3. Sql \n 4.Website \n press 0 to try again\n")

    if typ in ["1", "excel", "2", "csv"]:
        print("For convenience you can save the document on desktop and just enter the name of the file")
        print("If it's saved somewhere else then kindly just enter the location of the document")
        location = input("Enter document location: ")
        if len(location) < 10:
            location = r"C:\Users\krish\Desktop\\" + location

        if typ in ["1", "excel"]:
            location += ".xlsx"
            df = pd.read_excel(location)
            print(df)

        elif typ in ["2", "csv"]:
            location += ".csv"
            df = pd.read_csv(location)
            print(df)

    elif typ in ["3", "sql"]:
        h = input("Enter the host: ")
        u = input("Enter the user: ")
        p = input("Enter the password: ")
        d = input("Enter the database: ")
        db = c.connect(host=h, user=u, passwd=p, database=d)
        t = input("Enter the table name: ")
        query = f"SELECT * FROM {t}"
        df = pd.read_sql(query, con=db)
        print(df)

    elif typ in ["4", "website"]:
        location = input("Enter the URL of the DataFrame: ")
        df = pd.read_html(location)[0]  # Assumes the first table is the desired DataFrame
        print(df)

    elif typ == "0":
        collection()

    else:
        print("Invalid input. Please try again.")
        collection()

def axis():
    global x, y

    x = input("Enter the column name you want as x axis: ")
    if x not in df.columns:
        print("Invalid input for x axis. Please try again.")
        axis()

    while True:
        y = input("Enter the column name you want as y axis: ")
        if y not in df.columns:
            print("Invalid input for y axis. Please try again.")
        else:
            break

def graphs2d():
    pio.renderers.default = "browser"

    opt = input("Type of graph \n 1. Scatter \n 2. Histogram \n 3. Bar \n 4. Box \n 5. Heatmap \n Go back press 0 and 9 to exit \n")

    if opt in ["1", "scatter"]:
        fig = go.Figure(go.Scatter(x=df[x], y=df[y], mode='markers'))
    elif opt in ["2", "histogram"]:
        fig = go.Figure(go.Histogram(x=df[x]))
    elif opt in ["3", "bar"]:
        fig = go.Figure(go.Bar(x=df[x], y=df[y]))
    elif opt in ["4", "box"]:
        fig = go.Figure(go.Box(y=df[y]))
    elif opt in ["5", "heatmap"]:
        fig = go.Figure(go.Heatmap(z=df.pivot(index=y, columns=x, values=df.columns[0])))
    elif opt == "0":
        main()
        return
    elif opt == "9":
        print("Thanks for using the program.")
        return
    else:
        print("Invalid option. Try again.")
        graphs2d()
        return

    fig.show()
    graphs2d()

def graphs3d():
    pio.renderers.default = "browser"

    opt = input("Type of 3D graph \n 1. Scatter \n 2. Mesh \n Go back press 0 and 9 to exit \n")
    
    if opt == "1" or opt.lower() == "scatter":
        fig = go.Figure(go.Scatter3d(x=df[x], y=df[y], z=df[z], mode='markers'))
    elif opt == "2" or opt.lower() == "mesh":
        fig = go.Figure(go.Surface(x=df[x], y=df[y], z=df[z]))
    elif opt == "0":
        main()
        return
    elif opt == "9":
        print("Thanks for using the program.")
        return
    else:
        print("Invalid option. Try again.")
        graphs3d()
        return

    fig.show()
    graphs3d()

def main():
    print("------------------MENU--------------------")
    print("\nPlease select one of the options.")

    while True:
        opt = input(" 1. 2D Graphs \n 2. 3D Graphs \n To exit press 9 \n")

        if opt in ["1", "2D Graphs"]:
            collection()
            axis()
            graphs2d()

        elif opt in ["2", "3D Graphs"]:
            collection()
            axis()
            global z
            while True:
                z = input("Enter the column name you want as z axis: ")
                if z not in df.columns:
                    print("Invalid input for z axis. Please try again.")
                else:
                    break
            graphs3d()

        elif opt == "9":
            print("END OF PROGRAM")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
