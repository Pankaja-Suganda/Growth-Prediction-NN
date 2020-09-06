package com.example.automatedgreenhouse;

import android.support.annotation.NonNull;
import android.support.design.widget.Snackbar;
import android.view.View;
import android.widget.ProgressBar;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
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
    public static final String Monitor_Data = "Monitoring";
    public static final String Control_Data = "ControlingData";

    private FirebaseUser firebaseuser;
    private FirebaseAuth firebaseAuth = getInstance();
    private static Boolean State = false;

    private String User;
    private String Password;

    private FirebaseDatabase Database;
    private DatabaseReference DBReferance;
    private static List<Data_Monitor> DataMonitor = new ArrayList<>();
    private static long DataMonitor_Count;
    View context ;

    public interface DataStatus{
        void DataIsLoaded(List<Data_Monitor> Dmonitor, List<String> keys);
    }
    public DbConnection(String ParentNode) {
        Database = FirebaseDatabase.getInstance();
        DBReferance = Database.getReference("Monitoring");
    }
    public DbConnection() {
    }
    public DbConnection(String user, String password, View mcontext) {
        User = user;
        Password = password;
        context = mcontext;
    }
    public void SignInNewUser(final ProgressBar SignInPro) throws FirebaseAuthException {
        MainActivity activity = new MainActivity();
        firebaseAuth.createUserWithEmailAndPassword(User, Password).addOnCompleteListener(activity, new OnCompleteListener<AuthResult>() {
            @Override
            public void onComplete(@NonNull Task<AuthResult> task) {
                if (task.isSuccessful()) {
                    State =  true;
                    Snackbar.make(context, "Sign In Operation is Successfully Completed", Snackbar.LENGTH_LONG).show();
                } else {
                    State =  false;
                    Snackbar.make(context, task.getException().getMessage(), Snackbar.LENGTH_LONG).show();
                }
                SignInPro.setVisibility(ProgressBar.INVISIBLE);
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

    public void ReadData(final DataStatus datastatus) {
        DBReferance.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {

                    DataMonitor.clear();
                    List<String> keys = new ArrayList<>();
                    DataMonitor_Count = dataSnapshot.getChildrenCount();
                    for (DataSnapshot keyNodes : dataSnapshot.getChildren()) {
                        keys.add(keyNodes.getKey());
                        Data_Monitor DMonitor = keyNodes.getValue(Data_Monitor.class);
                        DataMonitor.add(DMonitor);
                    }
                datastatus.DataIsLoaded(DataMonitor,keys);
            }
            @Override
            public void onCancelled(DatabaseError databaseError) {
            }
        });
    }

    public static String getMonitor_Data() {
        return Monitor_Data;
    }

    public static String getControl_Data() {
        return Control_Data;
    }

    public FirebaseUser getFirebaseuser() {
        return firebaseuser;
    }

    public void setFirebaseuser(FirebaseUser firebaseuser) {
        this.firebaseuser = firebaseuser;
    }

    public FirebaseAuth getFirebaseAuth() {
        return firebaseAuth;
    }

    public void setFirebaseAuth(FirebaseAuth firebaseAuth) {
        this.firebaseAuth = firebaseAuth;
    }

    public  Boolean getState() {
        return State;
    }


    public  void setState(Boolean state) {
        State = state;
    }

    public String getUser() {
        return User;
    }

    public void setUser(String user) {
        User = user;
    }

    public String getPassword() {
        return Password;
    }

    public void setPassword(String password) {
        Password = password;
    }

    public FirebaseDatabase getDatabase() {
        return Database;
    }

    public void setDatabase(FirebaseDatabase database) {
        Database = database;
    }

    public DatabaseReference getDBReferance() {
        return DBReferance;
    }

    public void setDBReferance(DatabaseReference DBReferance) {
        this.DBReferance = DBReferance;
    }

    public List<Data_Monitor> getDataMonitor() {
        return DataMonitor;
    }

    public void setDataMonitor(List<Data_Monitor> dataMonitor) {
        DataMonitor = dataMonitor;
    }

    public long getDataMonitor_Count() {
        return DataMonitor_Count;
    }

    public void setDataMonitor_Count(int dataMonitor_Count) {
        DataMonitor_Count = dataMonitor_Count;
    }

    public View getContext() {
        return context;
    }

    public void setContext(View context) {
        this.context = context;
    }
}
