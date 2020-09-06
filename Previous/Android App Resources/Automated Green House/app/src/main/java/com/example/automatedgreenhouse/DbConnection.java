package com.example.automatedgreenhouse;

import android.content.Intent;
import android.support.annotation.NonNull;
import android.support.design.widget.Snackbar;
import android.util.Log;
import android.view.View;
import android.widget.ListView;
import android.widget.ProgressBar;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.FirebaseException;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseAuthException;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.ArrayList;
import java.util.List;

import static com.google.firebase.auth.FirebaseAuth.*;


public class DbConnection {
    private static final String Monitor_Data = "Data_Monitor";
    private static final String Control_Data = "ControlingData";

    private FirebaseUser firebaseuser;
    private FirebaseAuth firebaseAuth = getInstance();
    private static Boolean State = false;

    private String User;
    private String Password;

    private FirebaseDatabase Database;
    private DatabaseReference DBReferance;
    private List<Data_Monitor> DataMonitor = new ArrayList<>();
    private long DataMonitor_Count;
    View context ;

    public interface DataStatus{
        void DataIsLoaded(List<Data_Monitor> Dmonitor, List<String> keys);
        void DataIsInsert();
        void DataIsUpdated();
        void DataIsDeleted();
    }
    public DbConnection(String ParentNode) {
        Database = FirebaseDatabase.getInstance();
        DBReferance = Database.getReference(ParentNode);
    }

    public void ReadData(final DataStatus dataStatus){
        DBReferance.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                DataMonitor.clear();
                List<String> keys = new ArrayList<>();
                DataMonitor_Count = dataSnapshot.getChildrenCount();
                for(DataSnapshot keyNodes : dataSnapshot.getChildren()){
                    keys.add(keyNodes.getKey());
                    Data_Monitor DMonitor = keyNodes.getValue(Data_Monitor.class);
                    DataMonitor.add(DMonitor);
                }
                dataStatus.DataIsLoaded(DataMonitor,keys);
            }

            @Override
            public void onCancelled(DatabaseError databaseError) {

            }
        });
    }

    public DbConnection() {
    }

    public DbConnection(String user, String password, View mcontext) {
        User = user;
        Password = password;
        context = mcontext;
    }


    public void SignInNewUser() throws FirebaseAuthException {
        MainActivity activity = new MainActivity();
        firebaseAuth.createUserWithEmailAndPassword(User, Password).addOnCompleteListener(activity, new OnCompleteListener<AuthResult>() {
            @Override
            public void onComplete(@NonNull Task<AuthResult> task) {
                if (task.isSuccessful()) {
                    Snackbar.make(context, "Sign In Operation is Successfully Completed", Snackbar.LENGTH_LONG).show();
                } else {
                    Snackbar.make(context, task.getException().getMessage(), Snackbar.LENGTH_LONG).show();
                }
            }
        });
    }
    public  void UserLogin(final ProgressBar LoginPro) throws FirebaseAuthException {
        final MainActivity activity = new MainActivity();
        firebaseAuth.signInWithEmailAndPassword(User, Password).addOnCompleteListener(activity, new OnCompleteListener<AuthResult>() {
            @Override
            public void onComplete(@NonNull Task<AuthResult> task) {
                if (task.isSuccessful()) {
                    State =  true;
                    firebaseuser = firebaseAuth.getCurrentUser();
                    Snackbar.make(context, firebaseAuth.getCurrentUser().getEmail() +"  Log In Operation is Successfully Completed", Snackbar.LENGTH_LONG).show();
                } else {
                    State = false;
                    Snackbar.make(context, task.getException().getMessage(), Snackbar.LENGTH_LONG).show();
                }
                LoginPro.setVisibility(ProgressBar.INVISIBLE);
            }
        });

    }
    public String WriteData()  {
        final String[] state = new String[1];
        FirebaseDatabase database = FirebaseDatabase.getInstance();
        DatabaseReference myRef = database.getReference("Test");
        final MainActivity activity = new MainActivity();
//        final Data_Monitor Data = new Data_Monitor("50", "60", "70", "80");
        String id = myRef.push().getKey();
//        myRef.child(id).setValue(Data);
        return id;
    }

}
