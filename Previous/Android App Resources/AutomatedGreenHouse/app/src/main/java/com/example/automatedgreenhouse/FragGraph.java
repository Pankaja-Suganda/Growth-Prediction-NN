package com.example.automatedgreenhouse;

import android.content.Context;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.app.Fragment;
import android.support.design.widget.Snackbar;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.google.firebase.auth.FirebaseAuthException;
import com.jjoe64.graphview.CursorMode;
import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.GridLabelRenderer;
import com.jjoe64.graphview.RectD;
import com.jjoe64.graphview.Viewport;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.DataPointInterface;
import com.jjoe64.graphview.series.LineGraphSeries;
import com.jjoe64.graphview.series.OnDataPointTapListener;
import com.jjoe64.graphview.series.PointsGraphSeries;
import com.jjoe64.graphview.series.Series;

import java.nio.LongBuffer;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import android.widget.Toast;

/**
 * A simple {@link Fragment} subclass.
 * Activities that contain this fragment must implement the
 * {@link FragGraph.OnFragmentInteractionListener} interface
 * to handle interaction events.
 * Use the {@link FragGraph#newInstance} factory method to
 * create an instance of this fragment.
 */
public class FragGraph extends Fragment {
    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";

    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;


    GraphView Maingraph, TemVsHeightGraph, HumVsHeightGraph, LitVsHeightGraph, MoisVsHeightGraph;

    private OnFragmentInteractionListener mListener;

    public FragGraph() {
        // Required empty public constructor

    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param param1 Parameter 1.
     * @param param2 Parameter 2.
     * @return A new instance of fragment FragGraph.
     */
    // TODO: Rename and change types and number of parameters
    public static FragGraph newInstance(String param1, String param2) {
        FragGraph fragment = new FragGraph();
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

        return inflater.inflate(R.layout.fragment_frag_graph, container, false);
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
    private void GraphFill(GraphView graph, List<Data_Monitor> dmonitor, List<String> keys, int AxisX, int AxisY, int color) {
        int Index = dmonitor.size()-1;
        LineGraphSeries<DataPoint> series = new LineGraphSeries<DataPoint>();
        for(int i = 0;i<=Index;i++) {
            series.appendData(new DataPoint(dmonitor.get(i).GetData(AxisX),dmonitor.get(i).GetData(AxisY)), true, dmonitor.size());

        }
        series.setThickness(1);
        series.setDataPointsRadius(2);
        series.setColor(color);
        graph.addSeries(series);
    }

    private void GraphFill(GraphView graph, List<Data_Monitor> dmonitor, List<String> keys, int AxisX, int AxisY, List<String> Labels,int color) {
        try {
            int Index = dmonitor.size() - 1;
            LineGraphSeries<DataPoint> series = new LineGraphSeries<DataPoint>();
            List<Float> XAxis = new ArrayList<>(), YAxis = new ArrayList<>();
            for (int i = 0; i <= Index; i++) {
                XAxis.add( dmonitor.get(i).GetData(AxisX));
                YAxis.add( dmonitor.get(i).GetData(AxisY));
            }
            Log.d(" UnSorted XAxis", XAxis.toString());
            Log.d(" UnSorted YAxis", YAxis.toString());
            Collections.sort(XAxis);
            Collections.sort(YAxis);
            for (int i = 0; i <= Index; i++) {
                series.appendData(new DataPoint(XAxis.get(i), YAxis.get(i)), true, dmonitor.size());
            }

            Log.d("XAxis", XAxis.toString());
            Log.d("YAxis", YAxis.toString());
            series.setDrawAsPath(true);
            series.setDrawDataPoints(true);
            series.setBackgroundColor(Color.TRANSPARENT);
            series.setColor(color);
            series.setThickness(2);
            series.setDataPointsRadius(3);
            series.setDrawAsPath(true);
            Viewport viewport = graph.getViewport();

            viewport.setBackgroundColor(Color.argb((int) 0.5, 100, 100, 100));
            viewport.setScalable(true);
            viewport.setScalableY(true);
            viewport.setYAxisBoundsManual(true);
            viewport.setXAxisBoundsManual(true);
            viewport.setScrollable(true);
            viewport.setScrollableY(true);
            viewport.setMaxX((XAxis.get(XAxis.size() - 1)) + 5);
            viewport.setMinX(XAxis.get(0));
            viewport.setMaxY((YAxis.get(YAxis.size() - 1)) + 5);
            viewport.setMinY(0);
            viewport.setDrawBorder(true);
            graph.setDrawingCacheEnabled(true);
            GridLabelRenderer g = graph.getGridLabelRenderer();
            g.setGridColor(Color.GRAY);
            graph.setTitle(Labels.get(0));
            graph.setTitleColor(getResources().getColor(R.color.ColorText));
            g.setHorizontalLabelsColor(getResources().getColor(R.color.ColorText));
            g.setVerticalLabelsColor(getResources().getColor(R.color.ColorText));
            g.setVerticalAxisTitleColor(getResources().getColor(R.color.ColorText));
            g.setHorizontalAxisTitleColor(getResources().getColor(R.color.ColorText));
            g.setHorizontalLabelsColor(getResources().getColor(R.color.ColorText));
            g.setHorizontalAxisTitle(Labels.get(1));
            g.setVerticalAxisTitle(Labels.get(2));
            graph.removeAllSeries();
            graph.addSeries(series);
        } catch (IllegalArgumentException  e) {
            MainActivity actNew = new MainActivity();
            Toast.makeText(actNew, e.getMessage(), Toast.LENGTH_LONG).show();
        }
        catch (NullPointerException e) {
            MainActivity actNew = new MainActivity();
            Toast.makeText(actNew, e.getMessage(), Toast.LENGTH_LONG).show();
        }
    }
    @Override
    public void onViewCreated(View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        Maingraph = (GraphView)getView().findViewById(R.id.MainGraph) ;
        TemVsHeightGraph = (GraphView)getView().findViewById(R.id.TemVsHeightGraph) ;
        HumVsHeightGraph = (GraphView)getView().findViewById(R.id.HumVsHeightGraph) ;
        LitVsHeightGraph = (GraphView)getView().findViewById(R.id.LightVsHeightGraph) ;
        MoisVsHeightGraph = (GraphView)getView().findViewById(R.id.MoisVsHeightGraph) ;
        Navigate navigate = new Navigate();
            navigate.test(new Navigate.Datatributor() {
                @Override
                public void MainDataIsLoaded(List<Data_Monitor> Dmonitor, List<String> keys) {
                    GraphFill(Maingraph, Dmonitor, keys, Data_Monitor.cHeight, Data_Monitor.cDate, new ArrayList<String>(Arrays.asList(
                                getResources().getString(R.string.Graph_Title_HeightVsDate),
                                getResources().getString(R.string.Title_Height),
                                getResources().getString(R.string.Title_Date))), Color.RED);
                        GraphFill(Maingraph,Dmonitor, keys,Data_Monitor.cWidth, Data_Monitor.cDate, Color.BLUE);
    //                    GraphFill(Maingraph,Dmonitor, keys,Data_Monitor.cArea, Data_Monitor.cDate, Color.YELLOW);

                        GraphFill(TemVsHeightGraph,Dmonitor, keys,Data_Monitor.cTemperature,Data_Monitor.cHeight, new ArrayList<String>(Arrays.asList(
                                getResources().getString(R.string.Graph_Title_TemperatureVsHeight), getResources().getString(R.string.Title_Temperature),
                                getResources().getString(R.string.Title_Height))), Color.RED);
                        GraphFill(HumVsHeightGraph,Dmonitor, keys,Data_Monitor.cHumidity, Data_Monitor.cHeight, new ArrayList<String>(Arrays.asList(
                                getResources().getString(R.string.Graph_Title_HumidityVsHeight),
                                getResources().getString(R.string.Title_HumidityV),
                                getResources().getString(R.string.Title_Height))), Color.GREEN);
                        GraphFill(LitVsHeightGraph,Dmonitor, keys,Data_Monitor.cLight,Data_Monitor.cHeight, new ArrayList<String>(Arrays.asList(
                                getResources().getString(R.string.Graph_Title_LightVSHeight),
                                getResources().getString(R.string.Title_Light),
                                getResources().getString(R.string.Title_Height))), Color.BLUE);
                        GraphFill(MoisVsHeightGraph,Dmonitor, keys,Data_Monitor.cMoisture, Data_Monitor.cHeight, new ArrayList<String>(Arrays.asList(
                                getResources().getString(R.string.Graph_Title_MoistureVSHeight),
                                getResources().getString(R.string.Title_Moisture),
                                getResources().getString(R.string.Title_Height))), Color.YELLOW);
                    }
                });

    }


    @Override
    public void onDetach() {
        super.onDetach();
        mListener = null;
    }

    public interface OnFragmentInteractionListener {
        // TODO: Update argument type and name
        void onFragmentInteraction(Uri uri);
    }

}
