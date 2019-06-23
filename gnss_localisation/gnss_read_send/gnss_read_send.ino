#define HF_MAX_BUFFER_MSG_SIZE (250)

char buff[12][100]; //Initialized variable to store recieved data
char b2[7];
char gga[] = "$GNGGA";
char gll[] = "$GNGLL";
char * pch; 
char separated[20];
char *north;
char *east;
const char *separator = ",";
unsigned long time_send;
unsigned long time_check;
unsigned long time_delta;


void setup() {
  Serial.begin(19200);

}

void loop() {
  //Serial.println("eloloe");
  time_check = millis();
  time_delta = time_check - time_send;
  
  if (Serial.available() && (time_delta>10000)){
  //if (Serial.available() ){
    
    for (int i=0; i<12; i++){
      Serial.readBytesUntil('\n', buff[i], 100);
    }
    
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
        /*
          Serial.print("N: ");
          Serial.println(north);
          Serial.print("E: ");
          Serial.println(east);
          */
          strcat(north, separator);
          strcat(north, east);
          //Serial.println(north);
          //north1 = (String) ("5555.19563,02100.57196");
          //String msg;
          //msg = (String) ("<GPS=\"") + north + (String) ("\"#>");
//          char msg = [];
          //msg = "<GPS=\"" + north + "\"#>";
          uint8_t buf_msg[HF_MAX_BUFFER_MSG_SIZE];
          sprintf(buf_msg, "<GPS=%s#>", north);
//          msg = strcat("<GPS=\"", north);
//          msg = strcat(msg, "\"#>");
          char *ptr1, *ptr2;
          ptr1 = (char*)buf_msg;
          ptr2 = strstr(ptr1, ">");
          int len_buf=ptr2-ptr1;
          
          uint8_t buf_to_send[HF_MAX_BUFFER_MSG_SIZE+1];
          memset(buf_to_send, 46, HF_MAX_BUFFER_MSG_SIZE+1);
          memcpy(buf_to_send, buf_msg, len_buf+1);
          buf_to_send[HF_MAX_BUFFER_MSG_SIZE-1]='\n';
          buf_to_send[HF_MAX_BUFFER_MSG_SIZE]=0;
          
          Serial.print((char*)buf_to_send);
          time_send = millis();
          
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
