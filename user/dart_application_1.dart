import 'dart:io';
import 'dart:convert';

dynamic update() async {
  var data;
  var updateFile = File("update").create();
  data = await Process.run('curl', [
    '-X',
    'POST',
    '--upload-file',
    'update',
    'http://192.168.137.185:8000'
  ]).then((ProcessResult pr) {
    data = json.decode(pr.stdout);
    return data;
  });
  return data;
}

void upload(String filePath) async {
  var data;
  data = await Process.run('curl',
      ['-X', 'POST', '--upload-file', filePath, 'http://192.168.137.185:8000']);
}

dynamic search(String searchWord) async {
  var data;
  String fileName = "search-" + searchWord;
  print(fileName);
  var searchFile = File(fileName).create();
  data = await Process.run('curl', [
    '-X',
    'POST',
    '--upload-file',
    fileName,
    'http://192.168.137.185:8000'
  ]).then((ProcessResult pr) {
    data = json.decode(pr.stdout);
    return data;
  });
  File(fileName).delete();
  return data;
}

main() async {
  //update data
  var data = await update();
  print(data);

  //search data
  var data1 = await search("wonderland");
  print(data1);

  //upload data
  upload(r"C:\Users\t8883217\Desktop\סיכום אינטרו.pdf");
}
