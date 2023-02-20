library(RSQLite)
conn <- dbConnect(SQLite(),"s16.sqlite")

# List all the tables available in the database
dbListTables(conn)

# Write the mtcars dataset into a table names mtcars_data
#dbWriteTable(conn, "cars_data", mtcars)

# QUERU
D <- dbGetQuery(conn, "SELECT * FROM ncbi_dat")

D$genome_components
