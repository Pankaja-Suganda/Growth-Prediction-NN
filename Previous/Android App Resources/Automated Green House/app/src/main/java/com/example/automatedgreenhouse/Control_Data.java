package com.example.automatedgreenhouse;

import android.app.FragmentManager;
import android.app.FragmentTransaction;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.NavigationView;
import android.support.design.widget.Snackbar;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;

public class Control_Data {
    private String Humidity;
    private String Moisture;
    private String Temperature;
    private String Light;

    public Control_Data() {
    }

    public Control_Data(String humidity, String moisture, String temperature, String light) {
        Humidity = humidity;
        Moisture = moisture;
        Temperature = temperature;
        Light = light;
    }

    public String getHumidity() {
        return Humidity;
    }

    public void setHumidity(String humidity) {
        Humidity = humidity;
    }

    public String getMoisture() {
        return Moisture;
    }

    public void setMoisture(String moisture) {
        Moisture = moisture;
    }

    public String getTemperature() {
        return Temperature;
    }

    public void setTemperature(String temperature) {
        Temperature = temperature;
    }

    public String getLight() {
        return Light;
    }

    public void setLight(String light) {
        Light = light;
    }

    public static class DashBoard extends AppCompatActivity
            implements NavigationView.OnNavigationItemSelectedListener {
        TextView UserName , Email;
        ImageView UserImage;
        FirebaseUser CurrentUser;
        @Override
        protected void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);
            setContentView(R.layout.activity_dash_board);
            Toolbar toolbar = findViewById(R.id.toolbar);
            setSupportActionBar(toolbar);
            FloatingActionButton fab = findViewById(R.id.fab);

            fab.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                            .setAction("Action", null).show();
                }
            });


            DrawerLayout drawer = findViewById(R.id.drawer_layout);
            NavigationView navigationView = findViewById(R.id.nav_view);
            ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                    this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
            drawer.addDrawerListener(toggle);
            toggle.syncState();
            navigationView.setNavigationItemSelectedListener(this);

            CurrentUser = FirebaseAuth.getInstance().getCurrentUser();
            View header = navigationView.getHeaderView(0);
            UserName = (TextView) header.findViewById(R.id.txtName);
            Email = (TextView) header.findViewById(R.id.txtEmail);
            UserImage = (ImageView) header.findViewById(R.id.UserImage);

            Uri uri = CurrentUser.getPhotoUrl();
            UserName.setText(CurrentUser.getDisplayName());
            Email.setText(CurrentUser.getEmail());


        }

        @Override
        public void onBackPressed() {
            DrawerLayout drawer = findViewById(R.id.drawer_layout);
            if (drawer.isDrawerOpen(GravityCompat.START)) {
                drawer.closeDrawer(GravityCompat.START);
            } else {
                super.onBackPressed();
            }
        }

        @Override
        public boolean onCreateOptionsMenu(Menu menu) {
            // Inflate the menu; this adds items to the action bar if it is present.
            getMenuInflater().inflate(R.menu.dash_board, menu);
            return true;
        }

        @Override
        public boolean onOptionsItemSelected(MenuItem item) {
            // Handle action bar item clicks here. The action bar will
            // automatically handle clicks on the Home/Up button, so long
            // as you specify a parent activity in AndroidManifest.xml.
            int id = item.getItemId();

            //noinspection SimplifiableIfStatement
            if(id == R.id.action_Sign_Out){
                FirebaseAuth.getInstance().signOut();
                Email.setText("User Email");
                UserName.setText("User Name");
                finish();
                Intent intent = new Intent(this,MainActivity.class);
                startActivity(intent);
            }
            else if(id == R.id.action_Exit){
    //            DashboardF dashboard = new DashboardF();
    //            loadFragment(dashboard);
    //            finish();
            }

            return super.onOptionsItemSelected(item);
        }

        @SuppressWarnings("StatementWithEmptyBody")
        @Override
        public boolean onNavigationItemSelected(MenuItem item) {
            // Handle navigation view item clicks here.
            int id = item.getItemId();
            MenuItem mitem = (MenuItem) findViewById(R.id.nav_dashboard);
            mitem.setOnMenuItemClickListener(new MenuItem.OnMenuItemClickListener() {
                @Override
                public boolean onMenuItemClick(MenuItem item) {
                    DashboardF dashboard = new DashboardF();
                    loadFragment(dashboard);
                    return true;
                }
            });
            if (id == R.id.nav_dashboard) {
                DashboardF dashboard = new DashboardF();
                loadFragment(dashboard);

            } else if (id == R.id.nav_Control) {
                Control control = new Control();
                loadFragment(control);
            } else if (id == R.id.nav_Variation) {
                Graphs graph = new Graphs();
                loadFragment(graph);
            }
            else{
                Graphs graph = new Graphs();
                loadFragment(graph);
            }
            Graphs graph = new Graphs();
            loadFragment(graph);

            DrawerLayout drawer = findViewById(R.id.drawer_layout);
            drawer.closeDrawer(GravityCompat.START);
            return true;
        }

        private void loadFragment(android.app.Fragment fragment){
            FragmentManager FragManager = getFragmentManager();
            FragmentTransaction FragTrans = FragManager.beginTransaction();
            FragTrans.replace(R.id.ContentFrm, fragment);
            FragTrans.show(fragment);
            FragTrans.commit();

        }
    }
}
