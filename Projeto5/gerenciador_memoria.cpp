#include <string>	//string
#include <iostream>	//cout
#include <memory>	//shared_ptr
#include <sstream>	//stringstream

using namespace std;

//Função que recupera a saída de um comando do terminal como string
string exec(const char* cmd) {
    array<char, 128> buffer;
    string result;
    shared_ptr<FILE> pipe(popen(cmd, "r"), pclose);
    if (!pipe) throw runtime_error("popen() failed!");
    while (!feof(pipe.get())) {
        if (fgets(buffer.data(), 128, pipe.get()) != nullptr)
            result += buffer.data();
    }
    result.erase(result.end()-1);
    return result;
}

void gerarGrafico(float pct_usado){
	for(int i = 0; i < pct_usado; i++){
		cout << "#";
	}
    cout << " " << pct_usado << "% usados" << endl;
}

void funcaoGenerica(string comando, string memoria){
	string saida = exec(comando.c_str());
   	stringstream s1 (saida);
   	string total, usado;

   	s1 >> total;
   	s1 >> usado;

	cout << endl << memoria << total << " kB" << endl;

	float pct_usado = (float) stoi(usado) / stoi(total) * 100;

	gerarGrafico(pct_usado);
}

int main(){

	funcaoGenerica("free | grep -n ^ | grep ^2 | awk '{print $2 FS $3}'", "Memória Principal: ");

	string cache = exec("free | grep -n ^ | grep ^2 | awk '{print $6}'");
   	cout << endl << "Memória Cache: "<< cache << " kB" << endl;

   	funcaoGenerica("free | grep -n ^ | grep ^3 | awk '{print $2 FS $3}'", "Swap: ");

	string usuario = exec("users");
	string cmd = "ps -f -u "+ usuario;
	string comando = cmd +" | grep -v '"+ cmd +"' | grep -v 'grep' | grep -v 'awk' | awk '{print $2}'";
	string saida = exec(comando.c_str());

	stringstream s2 (saida);
	string pid;
	s2 >> pid; //Descartando a linha de título PID

	cout << endl << "Falta de página por processo:" << endl;
	s2 >> pid;
	comando = "ps -o user,pid,min_flt,maj_flt " + pid;
	saida = exec(comando.c_str());
	cout << saida << endl; //Exibindo a primeira linha com títulos PID, MINFL, MAJFL

	while(!s2.eof()){
		s2 >> pid;
		comando = "ps -o user,pid,min_flt,maj_flt " + pid + " | grep -n ^ | grep ^2:";
		saida = exec(comando.c_str());
		cout << saida.erase(0,2) << endl;
	}
	
	return 0;
}