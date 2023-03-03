from sqlToFasta import queryToFasta

entry = "Brucella pseudintermedia"
queryToFasta(table_to_get_seq = "s16full_sequence", 
                    join_table = "species2s16full_sequence", 
                    WHERE = f"")