import paramiko

class SFPTService():
    """docstring for SftoService."""
    def __init__(self,host,port,user,password):
        
        self._host = host
        self._port = int(port)
        self._user=user
        self._password = password 
        self.trasport = None
        self.sftp = None
    
    def connet(self):
        try:
            self.trasport = paramiko.Transport((self._host,self._port))
            self.trasport.connect(username=self._user,password=self._password)
            self.sftp = paramiko.SFTPClient.from_transport(self.trasport)
            print(f"Connectando a SFTP: {self._host}")
        except paramiko.AuthenticationException as e:
            self.close()
            raise "Error: Usuario o contraseña incorrectos."
        except paramiko.SSHException as e:
            self.close()
            raise f"Error de protocolo SSH: {e}"
        except Exception as e :
            self.close()
            raise f"Erro inesperado al conectar: { e}"

    def upload_file(self,local_path,remote_path):
        try:
            if self.sftp:
                self.sftp.put(local_path,remote_path)
        except FileExistsError as e:
            raise f"Error {e}"
        except IOError as io_error:
            raise   f"Error de E/S (Ruta remota valida?): { io_error}"
        except Exception as e  :
            raise f"Error al subir archivo: {e}"
    def close (self):
        if self.sftp: self.sftp.close()
        if self.trasport: self.trasport.close()
        raise f"Conexion Cerrada!!"