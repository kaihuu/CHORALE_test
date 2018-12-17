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
        SELECT COUNT(*), SUM(LOST_ENERGY)
        FROM ECOLOG_Doppler AS ECOLOG, SEMANTIC_LINKS, TRIPS_Doppler AS TRIPS
        WHERE ECOLOG.DRIVER_ID = 17 AND SEMANTIC_LINKS.SEMANTIC_LINK_ID = ? AND SEMANTIC_LINKS.LINK_ID = ECOLOG.LINK_ID
        AND ECOLOG.TRIP_DIRECTION = ? AND TRIPS.TRIP_ID = ECOLOG.TRIP_ID
		AND NOT EXISTS
		(SELECT *
		FROM ANNOTATION_Doppler AS ANNOTATION
		WHERE ECOLOG.TRIP_ID = ANNOTATION.TRIP_ID AND ECOLOG.JST >= ANNOTATION.START_TIME AND ECOLOG.JST <= ANNOTATION.END_TIME)
        GROUP BY TRIPS.TRIP_ID
		ORDER BY SUM(LOST_ENERGY)
        """
        return query

    @classmethod
    def QueryStringSpecial333outward1(self):
        query = """
        SELECT COUNT(*), SUM(LOST_ENERGY)
        FROM ECOLOG_Doppler AS ECOLOG, SEMANTIC_LINKS, TRIPS_Doppler AS TRIPS
        WHERE ECOLOG.DRIVER_ID = 17 AND SEMANTIC_LINKS.SEMANTIC_LINK_ID = ? AND SEMANTIC_LINKS.LINK_ID = ECOLOG.LINK_ID
        AND ECOLOG.TRIP_DIRECTION = ? AND TRIPS.TRIP_ID = ECOLOG.TRIP_ID
		AND NOT EXISTS
		(SELECT *
		FROM ANNOTATION_Doppler AS ANNOTATION
		WHERE ECOLOG.TRIP_ID = ANNOTATION.TRIP_ID AND ECOLOG.JST >= ANNOTATION.START_TIME AND ECOLOG.JST <= ANNOTATION.END_TIME)
        GROUP BY TRIPS.TRIP_ID
		HAVING COUNT(*) > 170
		ORDER BY SUM(LOST_ENERGY)
        """
        return query

    @classmethod
    def QueryStringSpecial333outward2(self):
        query = """
        SELECT COUNT(*), SUM(LOST_ENERGY)
        FROM ECOLOG_Doppler AS ECOLOG, SEMANTIC_LINKS, TRIPS_Doppler AS TRIPS
        WHERE ECOLOG.DRIVER_ID = 17 AND SEMANTIC_LINKS.SEMANTIC_LINK_ID = ? AND SEMANTIC_LINKS.LINK_ID = ECOLOG.LINK_ID
        AND ECOLOG.TRIP_DIRECTION = ? AND TRIPS.TRIP_ID = ECOLOG.TRIP_ID
		AND NOT EXISTS
		(SELECT *
		FROM ANNOTATION_Doppler AS ANNOTATION
		WHERE ECOLOG.TRIP_ID = ANNOTATION.TRIP_ID AND ECOLOG.JST >= ANNOTATION.START_TIME AND ECOLOG.JST <= ANNOTATION.END_TIME)
        GROUP BY TRIPS.TRIP_ID
		HAVING COUNT(*) <= 170
		ORDER BY SUM(LOST_ENERGY)
        """
        return query

    @classmethod
    def QueryStringSpecial337outward1(self):
        query = """
        SELECT COUNT(*), SUM(LOST_ENERGY)
        FROM ECOLOG_Doppler AS ECOLOG, SEMANTIC_LINKS, TRIPS_Doppler AS TRIPS
        WHERE ECOLOG.DRIVER_ID = 17 AND SEMANTIC_LINKS.SEMANTIC_LINK_ID = ? AND SEMANTIC_LINKS.LINK_ID = ECOLOG.LINK_ID
        AND ECOLOG.TRIP_DIRECTION = ? AND TRIPS.TRIP_ID = ECOLOG.TRIP_ID
		AND NOT EXISTS
		(SELECT *
		FROM ANNOTATION_Doppler AS ANNOTATION
		WHERE ECOLOG.TRIP_ID = ANNOTATION.TRIP_ID AND ECOLOG.JST >= ANNOTATION.START_TIME AND ECOLOG.JST <= ANNOTATION.END_TIME)
        GROUP BY TRIPS.TRIP_ID
		HAVING COUNT(*) > 170
		ORDER BY SUM(LOST_ENERGY)
        """
        return query

    @classmethod
    def QueryStringSpecial337outward2(self):
        query = """
        SELECT COUNT(*), SUM(LOST_ENERGY)
        FROM ECOLOG_Doppler AS ECOLOG, SEMANTIC_LINKS, TRIPS_Doppler AS TRIPS
        WHERE ECOLOG.DRIVER_ID = 17 AND SEMANTIC_LINKS.SEMANTIC_LINK_ID = ? AND SEMANTIC_LINKS.LINK_ID = ECOLOG.LINK_ID
        AND ECOLOG.TRIP_DIRECTION = ? AND TRIPS.TRIP_ID = ECOLOG.TRIP_ID
		AND NOT EXISTS
		(SELECT *
		FROM ANNOTATION_Doppler AS ANNOTATION
		WHERE ECOLOG.TRIP_ID = ANNOTATION.TRIP_ID AND ECOLOG.JST >= ANNOTATION.START_TIME AND ECOLOG.JST <= ANNOTATION.END_TIME)
        GROUP BY TRIPS.TRIP_ID
		HAVING COUNT(*) <= 170
		ORDER BY SUM(LOST_ENERGY)
        """
        return query

    @classmethod
    def QueryStringforECG(self):
        query = """
        SELECT COUNT(*), SUM(LOST_ENERGY), SUM(ABS(CONVERT_LOSS)),
		SUM(ABS(REGENE_LOSS)), SUM(ENERGY_BY_AIR_RESISTANCE), SUM(ENERGY_BY_ROLLING_RESISTANCE), TRIPS.TRIP_ID
        FROM ECOLOG_Doppler AS ECOLOG, SEMANTIC_LINKS, TRIPS_Doppler AS TRIPS
        WHERE ECOLOG.DRIVER_ID = 17 AND SEMANTIC_LINKS.SEMANTIC_LINK_ID = ? AND SEMANTIC_LINKS.LINK_ID = ECOLOG.LINK_ID
        AND ECOLOG.TRIP_DIRECTION = ? AND TRIPS.TRIP_ID = ECOLOG.TRIP_ID
        AND NOT EXISTS
		(SELECT *
		FROM ANNOTATION_Doppler AS ANNOTATION
		WHERE ECOLOG.TRIP_ID = ANNOTATION.TRIP_ID AND ECOLOG.JST >= ANNOTATION.START_TIME AND ECOLOG.JST <= ANNOTATION.END_TIME)
        GROUP BY TRIPS.TRIP_ID
		ORDER BY SUM(LOST_ENERGY)
        """
        return query

    @classmethod
    def QueryStringGetSemantics(self):
        query = """
        SELECT DISTINCT SEMANTIC_LINK_ID, SEMANTICS
        FROM SEMANTIC_LINKS
        WHERE SEMANTIC_LINK_ID = ?
        """
        return query

    @classmethod
    def QueryStringGetEndPoints(self):
        query = """
        SELECT SEMANTIC_LINK_ID, ENDPOINTS_OF_SEMANTIC_LINKS.DIRECTION, 
		CASE WHEN ENDPOINTS_OF_SEMANTIC_LINKS.LATITUDE IS NULL THEN LINKS.LATITUDE ELSE ENDPOINTS_OF_SEMANTIC_LINKS.LATITUDE END, 
		CASE WHEN ENDPOINTS_OF_SEMANTIC_LINKS.LONGITUDE IS NULL THEN LINKS.LONGITUDE ELSE ENDPOINTS_OF_SEMANTIC_LINKS.LONGITUDE END
        FROM ENDPOINTS_OF_SEMANTIC_LINKS, LINKS
        WHERE ENDPOINTS_OF_SEMANTIC_LINKS.NODE_ID = LINKS.NODE_ID AND ENDPOINTS_OF_SEMANTIC_LINKS.LINK_ID = LINKS.LINK_ID
		AND SEMANTIC_LINK_ID = ?
        ORDER BY DIRECTION
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