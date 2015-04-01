import falcon
import MySQLdb
import json
import settings

class TesResource:
	def on_get(self, req, resp):
		try:
			db = MySQLdb.connect(**settings.dbConfig)
			cursor = db.cursor(MySQLdb.cursors.DictCursor)
			
			q = ("SELECT * FROM tes")
			cursor.execute(q)
			rows = cursor.fetchall()
			
			output = {'tes': []}
			for row in rows:
				data = {
						"id": row['id'],
						"field1": row['field1'],
						"field2": row['field2']
					   }
				output['tes'].append(data)
			
			resp.status = falcon.HTTP_200
			resp.body = json.dumps(output, encoding='utf-8')
			cursor.close()
			db.close()
		
		except Exception as e:
			resp.body = json.dumps({'error':str(e)})
			resp.status = falcon.HTTP_500
			return resp
			
	def on_post(self, req, resp):
		try:
			db = MySQLdb.connect(**settings.dbConfig)
			cursor = db.cursor()

			raw_json = req.stream.read()
			data = json.loads(raw_json, encoding='utf-8')

			q = """INSERT INTO tes (field1, field2) VALUES(%s,%s)"""

			cursor.execute(q, (data['field1'], data['field2']))
			db.commit()
			cursor.close()

			output = {
				'status': "Data berhasil disimpan"
			}
			resp.status = falcon.HTTP_200
			data_resp = json.dumps(output, encoding='utf-8')
			resp.body = data_resp
			db.close()
		
		except Exception as e:
			db.rollback()
			resp.body = json.dumps({'error':str(e)})
			resp.status = falcon.HTTP_500
			return resp

	def on_put(self, req, resp):
		try:
			db = MySQLdb.connect(**settings.dbConfig)
			cursor = db.cursor()

			raw_json = req.stream.read()
			data = json.loads(raw_json, encoding='utf-8')
			
			q = """UPDATE `tes` SET `field1`=%s, `field2`=%s WHERE id=%s"""

			cursor.execute(q, (data['field1'], data['field2'], data['id']))
			db.commit()
			cursor.close()
			output = {
				'status': "Data berhasil diubah"
			}
			resp.status = falcon.HTTP_200
			data_resp = json.dumps(output, encoding='utf-8')
			resp.body = data_resp
			db.close()
			
		except Exception as e:
			db.rollback()
			resp.body = json.dumps({'error':str(e)})
			resp.status = falcon.HTTP_500
			return resp
			
	def on_delete(self, req, resp):
		try:
			id = req.get_param('id')
			if id is None or id == "":
				resp.body = json.dumps({'error':'Parameter id kosong'})
				resp.status = falcon.HTTP_500
				return resp
		
			db = MySQLdb.connect(**settings.dbConfig)
			cursor = db.cursor()

			q = """DELETE FROM `tes` WHERE id=%s"""

			cursor.execute(q, (id,))
			db.commit()
			cursor.close()
			output = {
				'status': "Data berhasil dihapus"
			}
			resp.status = falcon.HTTP_200
			data_resp = json.dumps(output, encoding='utf-8')
			resp.body = data_resp
		
		except Exception as e:
			db.rollback()
			resp.body = json.dumps({'error':str(e)})
			resp.status = falcon.HTTP_500
			return resp
