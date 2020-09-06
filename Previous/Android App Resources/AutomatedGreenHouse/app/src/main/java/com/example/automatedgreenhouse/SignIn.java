package com.example.automatedgreenhouse;

import android.content.Context;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.support.annotation.NonNull;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ProgressBar;

import com.firebase.client.Firebase;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseAuthException;
import com.google.firebase.auth.FirebaseUser;

public class SignIn extends AppCompatActivity {
    FirebaseAuth firebaseAuth;

    EditText txtEmail, txtPass, txtCPass;
    Button btnSign;
    ProgressBar SignProg;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sign_in);

        firebaseAuth = FirebaseAuth.getInstance();
        SignProg = (ProgressBar)findViewById(R.id.SignProg);
        txtEmail = (EditText) findViewById(R.id.txtEmailSign);
        txtPass = (EditText) findViewById(R.id.txtPasswordSign);
        txtCPass = (EditText)findViewById(R.id.txtCPasswordSign);

        btnSign = (Button) findViewById(R.id.btnSignin);
        btnSign.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(final View v) {

                if(isInternetConnection()) {
                    String email = txtEmail.getText().toString();
                    String Password = txtPass.getText().toString();
                    String CPassword = txtCPass.getText().toString();

                    if ((email.isEmpty() && Password.isEmpty() && CPassword.isEmpty())) {
                        txtEmail.setError("Please Enter Email..");
                        txtPass.setError("Please Enter Password..");
                        txtCPass.setError("Please Enter Password again..");
                        txtEmail.requestFocus();
                    } else if (email.isEmpty()) {
                        txtEmail.setError("Please Enter Email..");
                        txtEmail.requestFocus();
                    } else if (Password.isEmpty()) {
                        txtPass.setError("Please Enter Passwword..");
                        txtPass.requestFocus();
                    } else if (CPassword.isEmpty()) {
                        txtCPass.setError("Please Enter Password Again..");
                        txtCPass.requestFocus();
                    } else if (!(email.isEmpty() && Password.isEmpty() && CPassword.isEmpty())) {

                        DbConnection Signin = new DbConnection(email,Password,v);
                        SignProg.setVisibility(ProgressBar.VISIBLE);
                        try {
                            Signin.SignInNewUser(SignProg);
                            FirebaseAuth auth = FirebaseAuth.getInstance();
                            FirebaseUser user = auth.getCurrentUser();


                        } catch (FirebaseAuthException e) {
                            Snackbar.make(v,  e.getErrorCode() + "  " + e.getMessage(), Snackbar.LENGTH_LONG).setAction("Action", null).show();
                        }

                        if(Signin.getState()){
                            Navigate navigate = new Navigate();
                            Intent intent = new Intent(SignIn.this, navigate.getClass());
                            startActivity(intent);
                            finish();
                        }
                    }
                }
                else{
                    Snackbar.make(v, "You are not Connected.", Snackbar.LENGTH_LONG).setAction("Action", null).show();
                    Snackbar.make(v, "Please, switch on your mobile Data", Snackbar.LENGTH_LONG).setAction("Action", null).show();
                }
            }
        });
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
