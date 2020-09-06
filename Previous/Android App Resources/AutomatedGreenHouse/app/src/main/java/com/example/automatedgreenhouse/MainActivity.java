package com.example.automatedgreenhouse;

import android.content.Context;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.InputType;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TextView;

import com.firebase.client.Firebase;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseAuthException;
import com.google.firebase.auth.FirebaseUser;

public class MainActivity extends AppCompatActivity {
    Firebase url;
    public FirebaseAuth.AuthStateListener StateListener;
    public FirebaseUser FUser;
    FirebaseAuth firebaseAuth;

    EditText user, txtpass;
    Button btnLogin;
    ProgressBar LoginProg;
    ImageView bgapp, guitarimg;
    LinearLayout textsplash, llLogin;
    CheckBox CharChange;
    TextView sigining;

    @Override
    protected void onStart() {
        super.onStart();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Firebase.setAndroidContext(this);

        url = new Firebase("https://automated-green-house-fae2e.firebaseio.com/");
        firebaseAuth = FirebaseAuth.getInstance();
        LoginProg = (ProgressBar)findViewById(R.id.LoginProgress);
        user = (EditText) findViewById(R.id.txtuser);
        txtpass = (EditText) findViewById(R.id.txtPassword);
        bgapp = (ImageView)findViewById(R.id.bgapp);
        guitarimg = (ImageView) findViewById(R.id.guitarimg) ;
        textsplash = (LinearLayout)findViewById(R.id.textsplash) ;
        llLogin = (LinearLayout)findViewById(R.id.LL_Login);
        sigining = (TextView) findViewById(R.id.txtinfo);
        if(firebaseAuth.getCurrentUser() !=null){
            finish();
            Intent intent = new Intent(this,Navigate.class);
            startActivity(intent);
        }
        sigining.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, SignIn.class);
                startActivity(intent);
                finish();
            }
        });

        CharChange = (CheckBox) findViewById(R.id.chbcharchange);
        CharChange.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if(isChecked){
                    txtpass.setInputType(InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD);
                }
                else{
                    txtpass.setInputType(InputType.TYPE_TEXT_VARIATION_WEB_PASSWORD);

                }
            }
        });


        btnLogin = (Button) findViewById(R.id.btnLogin);
        btnLogin.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {

                if(isInternetConnection()) {
                    String email = user.getText().toString();
                    String Password = txtpass.getText().toString();

                    if (email.isEmpty() && Password.isEmpty()) {
                        user.setError("Please Enter Email Id..");
                        txtpass.setError("Please Enter Password");
                        user.requestFocus();
                    } else if (email.isEmpty()) {
                        user.setError("Please Enter Email Id..");
                        user.requestFocus();
                    } else if (Password.isEmpty()) {
                        txtpass.setError("Please Enter Password");
                        txtpass.requestFocus();
                    } else if (!(email.isEmpty() && Password.isEmpty())) {

                        DbConnection Login = new DbConnection(email,Password,v);
                        LoginProg.setVisibility(ProgressBar.VISIBLE);
                        try {
                            Login.UserLogin(LoginProg);
                        } catch (FirebaseAuthException e) {
                            Snackbar.make(v,  e.getErrorCode() + "  " + e.getMessage(), Snackbar.LENGTH_LONG).setAction("Action", null).show();
                        }

                        if(Login.getState()){
                            FUser = Login.getFirebaseuser();
                            llLogin.animate().translationY(200).alpha(0).setDuration(800).setStartDelay(50);
                            bgapp.animate().translationY(200).alpha(0).setDuration(800).setStartDelay(600);
                            finish();
                            Navigate navigate = new Navigate();
                            Intent intent = new Intent(MainActivity.this, navigate.getClass());
                            startActivity(intent);

                        }

                    }
                }
                else{
                    Snackbar.make(v, "Internet Connection is not on", Snackbar.LENGTH_LONG).setAction("Action", null).show();
                }
            }
        });
    }

    @Override
    protected void onStop() {
        super.onStop();

    }

    public void backGroundClick(android.view.View v){
        bgapp.animate().translationY(-1200).setDuration(800).setStartDelay(300);
        guitarimg.animate().translationX(-200).alpha(0).setDuration(600).setStartDelay(600);
        textsplash.animate().translationY(-800).alpha(0).setDuration(600).setStartDelay(300);
        llLogin.animate().translationY(-200).alpha(1).setDuration(600).setStartDelay(800);
        llLogin.setVisibility(View.VISIBLE);
    }


    public  boolean isInternetConnection() {

        boolean connected = false;
        ConnectivityManager connectivityManager = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        if (connectivityManager.getNetworkInfo(ConnectivityManager.TYPE_MOBILE).getState() == NetworkInfo.State.CONNECTED ||
                connectivityManager.getNetworkInfo(ConnectivityManager.TYPE_WIFI).getState() == NetworkInfo.State.CONNECTED) {
            return true;
        } else
            return false;
    }
}
