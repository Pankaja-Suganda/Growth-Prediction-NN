package com.example.automatedgreenhouse;

import android.content.Context;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.app.Fragment;
import android.os.Handler;
import android.support.design.widget.Snackbar;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;

import com.bumptech.glide.Glide;
import com.bumptech.glide.load.engine.GlideException;
import com.google.firebase.FirebaseException;
import com.google.firebase.auth.FirebaseAuthException;

import java.util.ArrayList;
import java.util.List;

import pl.pawelkleczkowski.customgauge.CustomGauge;


/**
 * A simple {@link Fragment} subclass.
 * Activities that contain this fragment must implement the
 * {@link DashBoard.OnFragmentInteractionListener} interface
 * to handle interaction events.
 * Use the {@link DashBoard#newInstance} factory method to
 * create an instance of this fragment.
 */
public class DashBoard extends Fragment {
    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";

    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;

    private OnFragmentInteractionListener mListener;

    private TextView Plant_Height, Plant_Width, Plant_Area;
    private TextView Ref_Height, Ref_Width, Ref_Area;
    private String ImgaUri;
    private ImageView Plant_Image;

    public DashBoard() {
        // Required empty public constructor
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param param1 Parameter 1.
     * @param param2 Parameter 2.
     * @return A new instance of fragment DashBoard.
     */
    // TODO: Rename and change types and number of parameters
    public static DashBoard newInstance(String param1, String param2) {
        DashBoard fragment = new DashBoard();
        Bundle args = new Bundle();
        args.putString(ARG_PARAM1, param1);
        args.putString(ARG_PARAM2, param2);
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {
            mParam1 = getArguments().getString(ARG_PARAM1);
            mParam2 = getArguments().getString(ARG_PARAM2);
        }

    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_dashboard, container, false);
    }

    // TODO: Rename method, update argument and hook method into UI event
    public void onButtonPressed(Uri uri) {
        if (mListener != null) {
            mListener.onFragmentInteraction(uri);
        }
    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);

        if (context instanceof OnFragmentInteractionListener) {
            mListener = (OnFragmentInteractionListener) context;
        }
//        else {
//            throw new RuntimeException(context.toString()
//                    + " must implement OnFragmentInteractionListener");
//        }
    }

    @Override
    public void onViewCreated(View view, Bundle savedInstanceState) {

            super.onViewCreated(view, savedInstanceState);
            new Handler().postDelayed(new Runnable() {

                @Override

                public void run() {
                    final TextView PlantHeight = (TextView) getView().findViewById(R.id.txtPlantHeight);
                    final TextView PlantWidth = (TextView) getView().findViewById(R.id.txtPlantwidth);
                    final TextView PlantArea = (TextView) getView().findViewById(R.id.txtPlantArea);
                    final TextView RefHeight = (TextView) getView().findViewById(R.id.txtRefHeight);
                    final TextView RefWidth = (TextView) getView().findViewById(R.id.txtRefWidht);
                    final TextView RefArea = (TextView) getView().findViewById(R.id.txtRefArea);
                    final ImageView PlantImage = (ImageView) getView().findViewById(R.id.imageView);

                    final CustomGauge TemGauge = (CustomGauge) getView().findViewById(R.id.TemGauge);
                    final CustomGauge HumGauge = (CustomGauge) getView().findViewById(R.id.HumGauge);
                    final CustomGauge MoisGauge = (CustomGauge) getView().findViewById(R.id.MoisGauge);
                    final CustomGauge LightGauge = (CustomGauge) getView().findViewById(R.id.LightGauge);
                    final TextView txtTemGauge = (TextView) getView().findViewById(R.id.txtTemGauge);
                    final TextView txtHumGauge = (TextView) getView().findViewById(R.id.txtHumGauge);
                    final TextView txtMoisGauge = (TextView) getView().findViewById(R.id.txtMoisGauge);
                    final TextView txtLightGauge = (TextView) getView().findViewById(R.id.txtLightGauge);

                    Navigate navigate = new Navigate();

                        navigate.test(new Navigate.Datatributor() {
                            @Override
                            public void MainDataIsLoaded(List<Data_Monitor> Dmonitor, List<String> keys) {

                                int Index = Dmonitor.size() - 1;
                                PlantHeight.setText(String.valueOf(Dmonitor.get(Index).getHeight()));
                                PlantWidth.setText(String.valueOf(Dmonitor.get(Index).getWidth()));
                                PlantArea.setText(String.valueOf(Dmonitor.get(Index).getArea()));
                                RefHeight.setText(String.valueOf(Dmonitor.get(Index).getRefHeight()));
                                RefWidth.setText(String.valueOf(Dmonitor.get(Index).getRefWidth()));
                                RefArea.setText(String.valueOf(Dmonitor.get(Index).getRefArea()));

                                TemGauge.setValue((int) Dmonitor.get(Index).getTemperature());
                                txtTemGauge.setText(String.valueOf(Dmonitor.get(Index).getTemperature()));
                                HumGauge.setValue((int) Dmonitor.get(Index).getHumidity());
                                txtHumGauge.setText(String.valueOf(Dmonitor.get(Index).getHumidity()));
                                MoisGauge.setValue((int) Dmonitor.get(Index).getMoisture());
                                txtMoisGauge.setText(String.valueOf(Dmonitor.get(Index).getMoisture()));
                                LightGauge.setValue((int) Dmonitor.get(Index).getLight());
                                txtLightGauge.setText(String.valueOf(Dmonitor.get(Index).getLight()));

                                Glide.with(getView()).
                                        load(Dmonitor.get(Index).getImageUri())
                                        .into(PlantImage);

                            }
                        });

                }

            }, 1000);
        }


    @Override
    public void onDetach() {
        super.onDetach();
        mListener = null;
    }

    /**
     * This interface must be implemented by activities that contain this
     * fragment to allow an interaction in this fragment to be communicated
     * to the activity and potentially other fragments contained in that
     * activity.
     * <p>
     * See the Android Training lesson <a href=
     * "http://developer.android.com/training/basics/fragments/communicating.html"
     * >Communicating with Other Fragments</a> for more information.
     */
    public interface OnFragmentInteractionListener {
        // TODO: Update argument type and name
        void onFragmentInteraction(Uri uri);
    }

}
