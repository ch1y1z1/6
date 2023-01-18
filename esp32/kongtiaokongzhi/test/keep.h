#pragma once
#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "../test/get_weather.h"
#include "../test/dht11.h"
#include <cstring>
#include <ctime>

float inrealfeel[50] = {0};
// 通过比较当前体感温度与之前的体感温度判断是否达到想要达到的室内体感温度
// 若未达到 则改变空调设置的温度来实现
void keepInRealFeel(int setInRealFeel, int &setTemp)
{
  for (int i = 0; i < 26; i++)
    inrealfeel[i] = inrealfeel[i + 1];
  inrealfeel[26] = get_temperature();
  if (abs(inrealfeel[26] - inrealfeel[25]) < 1 && abs(inrealfeel[26] - inrealfeel[24]) < 1 && abs(inrealfeel[26] - inrealfeel[23]) < 1 && abs(inrealfeel[26] - inrealfeel[22]) < 1 && abs(inrealfeel[26] - inrealfeel[21]) < 1 && abs(inrealfeel[26] - inrealfeel[20]) < 1 && abs(inrealfeel[26] - inrealfeel[19]) < 1 && abs(inrealfeel[26] - inrealfeel[18]) < 1 && abs(inrealfeel[26] - inrealfeel[17]) < 1)
  {
    if (inrealfeel[26] - setInRealFeel > 1)
      --setTemp;
    if (setInRealFeel - inrealfeel[26] > 1)
      ++setTemp;
  }
}