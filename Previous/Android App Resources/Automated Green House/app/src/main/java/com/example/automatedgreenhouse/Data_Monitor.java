package com.example.automatedgreenhouse;

import android.media.Image;
import java.util.List;

public class Data_Monitor {
    private String Height;
    private String Width;
    private String RefHeight;
    private String RefWidth;

    private String Humidity;
    private String Moisture;
    private String Temperature;
    private String Light;

    private Image Plant;

    public Data_Monitor(List<String> Data, Image plant) {
        Height = Data.get(0);
        Width = Data.get(1);
        Humidity = Data.get(2);
        Moisture = Data.get(3);
        Temperature = Data.get(4);
        Light = Data.get(5);
        RefHeight = Data.get(6);
        RefWidth = Data.get(7);
        Plant = plant;
    }

    public String getHeight() {
        return Height;
    }

    public String getWidth() {
        return Width;
    }

    public String getHumidity() {
        return Humidity;
    }

    public String getMoisture() {
        return Moisture;
    }

    public String getTemperature() {
        return Temperature;
    }

    public String getLight() {
        return Light;
    }
}
