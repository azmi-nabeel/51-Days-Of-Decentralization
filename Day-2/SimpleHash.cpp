/*Day-2:
Continuing with hashing techniques. Tried to implement a simple hashing technique in c++ instead of directly using hash functions in Python like I did yesterday. This hashing technique is much simpler
compared to SHA-256*/
#include <iostream>

using namespace std;

//This hash function takes the sum of ASCII values of the characters iin the string.
int sascii(string x, int M) {
     int i, sum;
     for (sum=0, i=0; i < x.length(); i++)
       sum += x[i];
     return sum % M;
   }

/* Drawback of this hashing function: 
1. Does not take the order of characters into account
2. The distribution of values wont be even.
  */

int main(){
  cout<<"Enter a string to hash"<<endl;
  string s;
  cin>>s;
  cout<<"The hash value for the string is: "<<sascii(s,16)<<endl;
  return 0;
}
