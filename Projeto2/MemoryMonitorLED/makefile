CXX			= arm-linux-gnueabihf-g++
INCLUDES	= -I/usr/arm-linux-gnuebihf/include/c++/4.8.4
CXXFLAGS	= -std=c++11 -O0 -g3 -Wall -fPIC -fmessage-length=0 -pthread $(CPPFLAGS) $(INCLUDES)
LDFLAGS		= -lpthread

PROG_NAME   = memoryLED
SRC_DIR     = ./src
BUILD_DIR   = ./build
BIN_DIR     = ./bin

SRC_LIST 	= $(wildcard $(SRC_DIR)/*.cpp)
OBJ_LIST 	= $(BUILD_DIR)/$(notdir $(SRC_LIST:.cpp=.o))

.PHONY: all clean $(PROG_NAME) compile

all: $(PROG_NAME)

compile: 
	$(CXX) -c $(CXXFLAGS) $(SRC_LIST) -c -o $(OBJ_LIST)

$(PROG_NAME): compile
	$(CXX) $(CXXFLAGS) $(OBJ_LIST) libBlack.a -o $(BIN_DIR)/$@

clean:
	rm -f $(BIN_DIR)/$(PROG_NAME) $(BUILD_DIR)/*.o