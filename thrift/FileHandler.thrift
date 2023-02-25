# FileHandler.thrift
namespace py filehandler

struct FileData {
  1: required string filename,
  2: required binary data
}

service FileHandler {
  FileData processFile(1: FileData file)
}

