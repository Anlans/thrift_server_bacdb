#! /usr/bin/env python3

from file_server.filehandler import FileHandler
from file_server.filehandler.ttypes import FileData

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

import os
import tempfile

class FileHandlerHandler(FileHandler.Iface):
  def processFile(self, file):
    # Save the incoming file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
      tmp_file.write(file.data)
      # tmp_file.flush()
      tmp_file.seek(0)
      print('tmp_file.read(): ' + str(tmp_file.read()))
      # Process the file using a script or function
      # output_file = process_file(tmp_file.name)
    output_file = tmp_file.name
    print('writed file success!')
      # Read the output file and return its contents
    with open(output_file, 'rb') as f:
      output_data = f.read()
      # Create and return a new FileData object with the output data
    output_file = file.filename
    return FileData(filename=os.path.basename(output_file), data=output_data)

def process_file(filename):
  # Use a script or function to process the file
  # Here we just create a new file with the same name and add a suffix
  # TODO write business logic
  output_file = filename + '.processed'
  with open(output_file, 'a', encoding='utf-8') as f:
    f.write('Processed file: ' + filename)
  with open(output_file, 'r', encoding='utf-8') as fr:
    fr.read()
  print('writing file...')
  return output_file

if __name__ == "__main__":
    handler = FileHandlerHandler()
    processor = FileHandler.Processor(handler)
    transport = TSocket.TServerSocket(port=29090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)

    print("Starting the server ...")
    server.serve()
    print('done.')
