package com.example.automatedgreenhouse;

import android.app.Fragment;
import android.app.FragmentManager;
import android.app.FragmentTransaction;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.util.AttributeSet;
import android.util.Log;
import android.view.View;
import android.support.v4.view.GravityCompat;
import android.support.v7.app.ActionBarDrawerToggle;
import android.view.MenuItem;
import android.support.design.widget.NavigationView;
import android.support.v4.widget.DrawerLayout;

import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;

import com.bumptech.glide.Glide;
import com.bumptech.glide.load.engine.GlideException;
import com.google.firebase.FirebaseException;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseAuthException;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.auth.UserInfo;

import java.util.List;

public class Navigate extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener {

    TextView UserName , Email;
    ImageView UserImage;
    FirebaseUser CurrentUser;


    @Override
    protected void onCreate(Bundle savedInstanceState)  {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_navigate);
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
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

        UserName.setText(CurrentUser.getProviderId());
        try {
            MakeLogin();
        }catch (GlideException e) {
            Snackbar.make(this.getCurrentFocus() ,e.getMessage(), Snackbar.LENGTH_LONG).show();
        }
        DashBoard Dashboard = new DashBoard();
        loadFragment(Dashboard);

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
        getMenuInflater().inflate(R.menu.navigate, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_Signout) {
            FirebaseAuth.getInstance().signOut();
            Email.setText("User Email");
            UserName.setText("User Name");
            finish();
            Intent intent = new Intent(this,MainActivity.class);
            startActivity(intent);
            return true;
        }
        else if(id == R.id.action_Exit){
            finish();
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();

        if (id == R.id.nav_Dashboard) {
            DashBoard Dashboard = new DashBoard();
            loadFragment(Dashboard);
//        } else if (id == R.id.nav_Control) {
//            Control control = new Control();
//            loadFragment(control);
        } else if (id == R.id.nav_Graph) {
            FragGraph graph = new FragGraph();
            loadFragment(graph);
        }

        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }


    private void loadFragment(android.app.Fragment fragment){
        FragmentManager FragManager = getFragmentManager();
        FragmentTransaction FragTrans = FragManager.beginTransaction();
        FragTrans.replace(R.id.ContentFrm, fragment);
        FragTrans.commit();

    }

    private void MakeLogin() throws GlideException {
        Email.setText(CurrentUser.getEmail());
        UserName.setText(CurrentUser.getDisplayName());
        Glide.with(this)
                .load(FirebaseAuth.getInstance().getCurrentUser().getPhotoUrl())
                .into(UserImage);

    }

    public interface Datatributor{
        void MainDataIsLoaded(List<Data_Monitor> Dmonitor, List<String> keys);
    }

    public void test(final Datatributor a)  {
        DbConnection read = new DbConnection(DbConnection.Control_Data);
            read.ReadData(new DbConnection.DataStatus() {
                @Override
                public void DataIsLoaded(List<Data_Monitor> Dmonitor, List<String> keys) {
                    a.MainDataIsLoaded(Dmonitor,keys);
                }
            });

    }


}
