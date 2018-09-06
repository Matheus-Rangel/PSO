#include <memory> //shared_ptr
#include <cstdio> // popen
#include <stdexcept> //runtime_error
#include <string>
#include <array>
#include <stdlib.h>
#include <unistd.h>

std::string exec(const char* cmd) {
    std::array<char, 128> buffer;
    std::string result;
    std::shared_ptr<FILE> pipe(popen(cmd, "r"), pclose);
    if (!pipe) throw std::runtime_error("popen() failed!");
    while (!feof(pipe.get())) {
        if (fgets(buffer.data(), 128, pipe.get()) != nullptr)
            result += buffer.data();
    }
    return result;
}
