from tabelas.config import Connection

# Herda de Connection pq vai utilizar os métodos de Connection
class PedidoTable(Connection):
    # CREATE
    def __init__(self):
        Connection.__init__(self)
        # sql = """
        # CREATE TABLE IF NOT EXISTS pedido(
        #     id_pedido SERIAL PRIMARY KEY NOT NULL,
        #     id_cliente INT NOT NULL,
        #     id_vendedor INT NOT NULL,
        #     custo FLOAT NOT NULL,
        #     data DATE NOT NULL DEFAULT CURRENT_DATE,
        #     forma_pagamento VARCHAR(255) NOT NULL,
        #     FOREIGN KEY (id_cliente) REFERENCES cliente (id_cliente),
        #     FOREIGN KEY (id_vendedor) REFERENCES vendedor (id_vendedor)
        # );
        # """
        # self.execute(sql)
        # self.commit()

    #READ/Search
    def read(self, select = '*', id_pedido = 0, id_cliente = 0, id_vendedor = 0, custo = 0, search_type = "id_cliente"):
        try:
            sql = f'SELECT {select} FROM pedido WHERE id_cliente = {id_cliente}'

            if search_type == "id_pedido":
                sql = f'SELECT {select} FROM pedido WHERE id_pedido = {id_pedido}'
            elif search_type == "id_vendedor":
                sql = f'SELECT {select} FROM pedido WHERE id_vendedor = {id_vendedor}'
            elif search_type == "custo":
                sql = f'SELECT {select} FROM pedido WHERE custo = {custo}'

            data = self.query(sql)
            if data:
                return data
            
            return False
        except Exception as error:
            print("Record not found in PedidoTable", error)

    def read_all(self, select = '*'):
        try:
            sql = f'SELECT {select} FROM pedido'

            data = self.query(sql)
            if data:
                return data
            
            return False
        except Exception as error:
            print("Record not found in PedidoTable", error)

    # UPDATE
    def update(self, desconto = 0.0, id_pedido = 0, id_cliente = 0, update_type = 'id_pedido'):
        try:
            sql = f'UPDATE pedido SET custo = custo * {1 - desconto} WHERE id_pedido = {id_pedido}' # desconto por pedido

            if update_type == 'id_cliente':
                sql = f'UPDATE pedido SET custo = custo * {1 - desconto} WHERE id_cliente = {id_cliente}' # desconto por cliente

            self.execute(sql)
            self.commit()
            # print("Record updated")
        except Exception as error:
            print("Error updating pedido", error)

    # INSERT
    def insert(self, id_cliente = 0, id_vendedor = 0, custo = 0, forma_pagamento = 'pix'):
        try:
            sql = f"INSERT INTO pedido (id_cliente, id_vendedor, custo, forma_pagamento) VALUES ({id_cliente}, {id_vendedor}, {custo}, '{forma_pagamento}')"

            self.execute(sql)
            self.commit()
        except Exception as error:
            print("Error inserting record", error)

    # DELETE
    def delete(self, id_pedido = 0):
        try:
            sql_search = f"SELECT * FROM pedido WHERE id_pedido = {id_pedido}"

            if not self.query(sql_search):
                return "Record not found on database"
            
            sql_delete = f"DELETE FROM pedido WHERE id_pedido = {id_pedido}"
            self.execute(sql_delete)
            self.commit()
            
        except Exception as error:
            print("Error deleting record", error)
