package com.example.automatedgreenhouse;

import android.media.Image;

import java.util.List;

public class Data_Monitor {

    public static final int cDate = 1;
    public static final int cHeight = 2;
    public static final int cWidth = 3;
    public static final int cArea = 4;
    public static final int cTemperature = 5;
    public static final int cHumidity = 6;
    public static final int cMoisture = 7;
    public static final int cLight = 8;

    private float Area;
    private float Date;
    private float Height;
    private float Humidity;
    private String ImageUri;
    private float Light;
    private float Moisture;
    private float RefArea;
    private float RefHeight;
    private float RefWidth;
    private float Temperature;
    private float Width;


    public Data_Monitor() {

    }



    public float GetData(int Index){
        float value = 0;
        switch(Index){
            case cDate:
                value = getDate();
                break;
            case cHeight:
                value = getHeight();
                break;
            case cWidth:
                value = getWidth();
                break;
            case cArea:
                value = getArea();
                break;
            case cTemperature:
                value = getTemperature();
                break;
            case cHumidity:
                value = getHumidity();
                break;
            case cMoisture:
                value = getMoisture();
                break;
            case cLight:
                value = getLight();
                break;

        }
        return value;
    }

    public float getArea() {
        return Area;
    }

    public void setArea(float area) {
        Area = area;
    }

    public float getDate() {
        return Date;
    }

    public void setDate(float date) {
        Date = date;
    }

    public float getHeight() {
        return Height;
    }

    public void setHeight(float height) {
        Height = height;
    }

    public float getHumidity() {
        return Humidity;
    }

    public void setHumidity(float humidity) {
        Humidity = humidity;
    }

    public String getImageUri() {
        return ImageUri;
    }

    public void setImageUri(String imageUri) {
        ImageUri = imageUri;
    }

    public float getLight() {
        return Light;
    }

    public void setLight(float light) {
        Light = light;
    }

    public float getMoisture() {
        return Moisture;
    }

    public void setMoisture(float moisture) {
        Moisture = moisture;
    }

    public float getRefArea() {
        return RefArea;
    }

    public void setRefArea(float refArea) {
        RefArea = refArea;
    }

    public float getRefHeight() {
        return RefHeight;
    }

    public void setRefHeight(float refHeight) {
        RefHeight = refHeight;
    }

    public float getRefWidth() {
        return RefWidth;
    }

    public void setRefWidth(float refWidth) {
        RefWidth = refWidth;
    }

    public float getTemperature() {
        return Temperature;
    }

    public void setTemperature(float temperature) {
        Temperature = temperature;
    }

    public float getWidth() {
        return Width;
    }

    public void setWidth(float width) {
        Width = width;
    }
}
