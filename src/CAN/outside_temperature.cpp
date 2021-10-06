#include "e90canbus.h"
#include "globals.h"

uint8_t outside_temp_frame[2] = {0x61, 0xFF};

const uint16_t CAN_ID = 0x2CA;

void canSendOutsideTemp()
{
    outside_temp_frame[0] = s_outside_temp * 2 + 80;
    CAN.sendMsgBuf(CAN_ID, 0, 2, outside_temp_frame);
}