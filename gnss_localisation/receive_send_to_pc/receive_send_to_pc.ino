//#define NMEA_MSG "$GNGLL"

char buff[12][100]; //Initialized variable to store recieved data
char b2[7];
char gga[] = "$GNGGA";
char gll[] = "$GNGLL";
char * pch; 
char separated[20];
char *north;
char *east;
const char *separator = ",";

void setup() {
  Serial.begin(19200);
}
void loop() {
  Serial.println("wowowo");
  /*
  String north1;
  north1 = (String) ("5555.19563,02100.57196");
  String msg;
  msg = (String) ("<GPS=\"") + north1 + (String) ("\"#>");
  Serial.println(msg);
  */
  if (Serial.available()){
    Serial.println("mmmmmmmm");
    
    for (int i=0; i<12; i++){
      Serial.readBytesUntil('\n', buff[i], 100);
    }
    Serial.println("buff");
    Serial.println(buff[1]);
    for (int i=0; i<12; i++){
      //strncpy(b2, buff[i], 6);
      for(int j=0; j<6; j++){
        b2[j] = buff[i][j];  
      }

      if(strcmp(b2, gll)==0){
        //Serial.println(buff[i]);
        pch = strtok(buff[i], ",");
        
        //while(pch!=NULL) {
        for(int k=0; pch!=NULL; k++){  
          //if(k==2){
          if(k==1){
            north = pch;
          }
          
          //if(k==4){
          if(k==3){  
            east = pch;
          }
          //Serial.println(pch);
          pch = strtok(NULL, ",");
        }
          //String msg;
          Serial.println(north);
          strcat(north, separator);
          strcat(north, east);
          Serial.println(north);
          //String north1;
          //north1 = (String) ("5555.19563,02100.57196");
          //msg = (String) ("<GPS=\"") + north1 + (String) ("\"#>\n");
          //Serial.println(msg);
      }
    }
  
  memset(north, 0, sizeof north);
  memset(east, 0, sizeof east);
  memset(separated, 0, sizeof separated);
  memset(b2, 0, sizeof b2);
  memset(buff, 0, sizeof buff);
  }
}
