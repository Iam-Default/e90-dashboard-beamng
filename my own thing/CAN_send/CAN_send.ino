// CAN Send Example
//

#include <mcp_can.h>
#include <SPI.h>

MCP_CAN CAN(9);     // Set CS to pin 10


void canSendIgnitionFrame(bool state){
  const uint16_t CAN_ID = 0x130;
  
  uint8_t ignition_frame_on[5] = {0x45, 0x42, 0x69, 0x8f, 0xE2};
  uint8_t ignition_frame_off[5] = {0x00, 0x00, 0xC0, 0x0f, 0xE2};
  
  if(state){
    CAN.sendMsgBuf(CAN_ID, 0, 5, ignition_frame_on);
    ignition_frame_on[4]++;
  }else{
    CAN.sendMsgBuf(CAN_ID, 0, 5, ignition_frame_off);
    ignition_frame_off[4]++;
  }
}

void canSendSteeringWheel(){
  const uint16_t CAN_ID = 0x0C4;
  uint8_t steering_wheel_frame[7] = {0x83, 0xFD, 0xFC, 0x00, 0x00, 0xFF, 0xF1};

  steering_wheel_frame[1] = 0;
  steering_wheel_frame[2] = 0;

  CAN.sendMsgBuf(CAN_ID, 0, 7, steering_wheel_frame);
}

void canSendFuel(uint16_t fuel){//Max Val: 0, Min Val: 1201.25
  uint8_t fuel_frame[5] = {0x00, 0x00, 0x00, 0x00, 0x00};

  const uint16_t CAN_ID = 0x349;

  uint16_t level = min(100+(fuel*8), 9710);
  fuel_frame[0] = level;
  fuel_frame[1] = (level >> 8);

  fuel_frame[2] = fuel_frame[0];
  fuel_frame[3] = fuel_frame[1];

  CAN.sendMsgBuf(CAN_ID, 0, 5, fuel_frame);
}

void canSendHandbrake(bool state){
  const uint16_t CAN_ID = 0x34F;
  
  uint8_t handbrake_frame[2] = {0xFE, 0xFF};
  
  if(state){
    handbrake_frame[0] = 0xFE;
  }else{
    handbrake_frame[0] = 0xFD;
  }
  CAN.sendMsgBuf(CAN_ID, 0, 2, handbrake_frame);
}
void setup()
{
  Serial.begin(115200);

  // Initialize MCP2515 running at 16MHz with a baudrate of 500kb/s and the masks and filters disabled.
  if(CAN.begin(MCP_ANY, CAN_100KBPS, MCP_8MHZ) == CAN_OK) Serial.println("MCP2515 Initialized Successfully!");
  else Serial.println("Error Initializing MCP2515...");

  CAN.setMode(MCP_NORMAL);   // Change to normal mode to allow messages to be transmitted
}


uint8_t lights_frame[3] = {0x04, 0x00, 0xf7};


const uint16_t CAN_ID_lights = 0x21A;

void loop()
{
  // send data:  ID = 0x100, Standard CAN Frame, Data length = 8 bytes, 'data' = array of data bytes to send
  canSendIgnitionFrame(true);
  canSendHandbrake(true);
  canSendSteeringWheel();
  canSendFuel(450);
  /*byte sndStat = CAN.sendMsgBuf(CAN_ID_lights, 0, 3, lights_frame);
  if(sndStat == CAN_OK){
    Serial.println("Message Sent Successfully!");
  } else {
    Serial.println("Error Sending Message...");
  }*/
  delay(200);   // send data per 100ms
}

/*********************************************************************************************************
  END FILE
*********************************************************************************************************/
