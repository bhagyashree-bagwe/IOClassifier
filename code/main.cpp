#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <iterator>
#include <unordered_map>
#include <string.h>

using namespace std;
template<char delimiter>
class WordDelimitedBy : public std::string
{};
std::string MAIN="main";
std::unordered_map<int,std::vector<std::string>> lineMap;
std::unordered_map<std::string,int> function_start_map;
std::unordered_map<std::string,int> function_end_map;
std::vector<string> split(string s, const char* delim) {
    char * dup = strdup(s.c_str());
    char * token = strtok(dup, delim);
    vector<string> tokens;
    while(token != NULL){
        tokens.push_back(string(token));
        token = strtok(NULL, delim);
    }
    free(dup);
    return tokens;
}
void iterate(std::string function){
    cout << "call function "<<function<<" start"<<endl;
    int start=-1,end=-1;
    auto iter=function_start_map.find(function);
    if(iter!=function_start_map.end()){
        start=iter->second;
    }
    iter=function_end_map.find(function);
    if(iter!=function_end_map.end()){
        end=iter->second;
    }
    //cout << start <<" "<<end<<endl;
    if(!(start==-1 || end==-1)){
        while(start<=end){
            auto iter2=lineMap.find(start);
            if(iter2!=lineMap.end()){
                std::vector<std::string> lines=iter2->second;
                for(auto line:lines){
                    std::vector<string> results=split(line,"#");
                    if(results[0].compare("CursorKind.CALL_EXPR")==0){
                        iterate(results[1].c_str());
                    }
                }
            }
            start++;
        }
    }
    cout << "call function "<<function<<" end"<<endl;
}
int main()
{
    lineMap=std::unordered_map<int,std::vector<std::string>>();
    function_start_map=std::unordered_map<std::string,int>();
    function_end_map=std::unordered_map<std::string,int>();
    ifstream in("../output.log");

    if(!in) {
        cout << "Cannot open input file.\n";
        return 1;
    }

    char str[255];
    std::string val;
    int i=1;
    in.getline(str, 255);
    while(in) {
        //cout<<str<<endl;
        val=std::string(str);
        std::vector<string> results=split(val,"#");
        if(results[0].compare("CursorKind.FUNCTION_DECL")==0 || results[0].compare("CursorKind.CXX_METHOD")==0){
            std::vector<string> results2=split(results[1],"(");
            //cout << "function " << results2[0]<<".\n";
            auto iter=function_start_map.find(results2[0]);
            auto iter2=function_end_map.find(results2[0]);
            int start=atoi(results[3].c_str());
            int end=atoi(results[4].c_str());
            if(iter!=function_start_map.end() && iter2!=function_end_map.end()){
                if(iter2->second - iter->second == 0 && iter->second !=start && iter2->second!=end){
                    function_start_map.erase(iter);
                    function_end_map.erase(iter2);
                }
            }

            function_start_map.insert({results2[0],start});
            function_end_map.insert({results2[0],end});
        }
        int line=atoi(results[2].c_str());
        auto iter2=lineMap.find(line);
        std::vector<std::string> lines;
        if(iter2!=lineMap.end()){
            lines=iter2->second;
            lineMap.erase(iter2);
        }
        lines.push_back(val);
        lineMap.insert({line,lines});
        in.getline(str, 255);
        i++;
    }
    iterate(MAIN);
    in.close();
    return 0;
}
