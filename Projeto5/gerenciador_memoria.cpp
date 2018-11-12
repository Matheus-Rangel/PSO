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

void memoriaTotal(){
	string memoriaTotal = exec("cat /proc/meminfo | grep -n ^ | grep ^1: | awk '{print $2}'");
	string memoriaLivre = exec("cat /proc/meminfo | grep -n ^ | grep ^2: | awk '{print $2}'");
	cout << endl << "Memória Total: "<< memoriaTotal << " kB" << endl;

	float pct_usado;
	if(stoi(memoriaTotal) != 0)
		pct_usado = (float) (stoi(memoriaTotal) - stoi(memoriaLivre)) / stoi(memoriaTotal) * 100;
	else
		pct_usado = 0;
	gerarGrafico(pct_usado);
}

void memoriaCache(){
	string cache = exec("cat /proc/meminfo | grep -n ^ | grep ^5: | awk '{print $2 FS $3}'");
	cout << endl << "Memória Cache: "<< cache << endl;
}

void memoriaLivre(){
	string swapTotal = exec("cat /proc/meminfo | grep -n ^ | grep ^15: | awk '{print $2}'");
	string swapLivre = exec("cat /proc/meminfo | grep -n ^ | grep ^16: | awk '{print $2}'");
	cout << endl << "Swap Total: "<< swapTotal << " kB" << endl;

	float pct_usado;
	if(stoi(swapTotal) != 0)
		pct_usado = (float) (stoi(swapTotal) - stoi(swapLivre)) / stoi(swapTotal) * 100;
	else
		pct_usado = 0;

	gerarGrafico(pct_usado);
}

stringstream processosPorUsuario(){

	//Obtem o usuario
	string usuario = exec("users");
	stringstream s1 (usuario);
	s1 >> usuario;

	//Pega os processos de tal usuario
	string cmd = "ps -f -u "+ usuario;
	string comando = cmd +" | grep -v '"+ cmd +"' | grep -v 'grep' | grep -v 'awk' | awk '{print $2}'";
	string saida = exec(comando.c_str());

	stringstream ss (saida);
	string pid;
	ss >> pid; //Descartando a linha de título PID

	return ss;
}

void informacoesPorProcessos(){
	stringstream ss = processosPorUsuario();

	string pid;
	ss >> pid;
	
	cout << endl << "Falta de página por processo:" << endl;
	string comando = "ps -o user,pid,min_flt,maj_flt,%mem " + pid;
	string saida = exec(comando.c_str());
	cout << saida << endl; //Exibindo a primeira linha com títulos PID, MINFL, MAJFL

	while(!ss.eof()){
		ss >> pid;
		comando = "ps -o user,pid,min_flt,maj_flt,%mem " + pid + " | grep -n ^ | grep ^2:";
		saida = exec(comando.c_str());
		cout << saida.erase(0,2) << endl;
	}

}

int main(){

	memoriaTotal();

	memoriaCache();

	memoriaLivre();
	
	informacoesPorProcessos();

	return 0;
}