import pyodbc

class DBAccessor:
    """DB Access"""

    config = "DRIVER={SQL Server};SERVER=ECOLOGDB2016;DATABASE=ECOLOGDBver3"

    @classmethod
    def ExecuteQuery(self, query):
        cnn = pyodbc.connect(self.config)
        cur = cnn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        cnn.close()
        return rows

    @classmethod
    def ExecuteQueryFromList(self, query, datalist):
        cnn = pyodbc.connect(self.config)
        cur = cnn.cursor()
        cur.execute(query, datalist)
        rows = cur.fetchall()
        cur.close()
        cnn.close()
        return rows

    @classmethod
    def QueryString(self):
        query = """
        DECLARE @id int
        SET @id = ?;

        SELECT TRIP_ID, SUM(LOST_ENERGY), COUNT(*), MIN(JST)
        FROM ECOLOG_Doppler_NotMM, SEMANTIC_LINKS
        WHERE ECOLOG_Doppler_NotMM.DRIVER_ID = 17 AND SEMANTIC_LINKS.SEMANTIC_LINK_ID = @id AND SEMANTIC_LINKS.LINK_ID = ECOLOG_Doppler_NotMM.LINK_ID
        AND ECOLOG_Doppler_NotMM.TRIP_DIRECTION = 'outward'
        GROUP BY TRIP_ID
        """
        return query 

    @classmethod
    def ExecuteManyInsert(self, query, dataList):
        cnn = pyodbc.connect(self.config)
        cur = cnn.cursor()
        cur.executemany(query, dataList)
        cur.commit()
        cur.close()
        cnn.close()

    @classmethod
    def QueryInsertString(self):
        query = "INSERT INTO GOOGLE_DISTANCE_MATRIX VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        return query