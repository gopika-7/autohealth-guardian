// AutoHealth Guardian - React Native Mobile Dashboard (Expo)
// Single-file starter app (App.js) + instructions below.
// This app is built for Expo (managed workflow) and uses react-native-chart-kit for charts.
// Features: summary cards, time-series charts, day detail, risk charts, file upload (DocumentPicker fallback), and simple heuristics.
// How to use: copy this file as `App.js` inside a new Expo project created with `npx expo init autohealth-mobile` (managed, blank template).

/*
Package.json dependencies (install after expo init):

expo install react-native-svg react-native-chart-kit
npm install axios
expo install expo-file-system expo-document-picker

Then run:

npm start

# or
expo start
cd D:\autohealth-guardian\autohealth-mobile
npm install
npm start
python -m http.server 8000

Open on your phone with Expo Go or run on emulator.
*/

import React, { useEffect, useState } from 'react';
import { SafeAreaView, View, Text, ScrollView, TouchableOpacity, StyleSheet, Dimensions, Platform } from 'react-native';
import { LineChart, BarChart } from 'react-native-chart-kit';
import * as DocumentPicker from 'expo-document-picker';
import * as FileSystem from 'expo-file-system';

const screenWidth = Dimensions.get('window').width;

const sampleData = {
  user_1: {
    telemetry: [
      { ts: '2025-11-06', steps: 3239, water_ml: 890, sleep_hours: 8.3, screen_minutes: 382 },
      { ts: '2025-11-07', steps: 3092, water_ml: 2172, sleep_hours: 5.0, screen_minutes: 185 },
      { ts: '2025-11-08', steps: 2185, water_ml: 1109, sleep_hours: 6.6, screen_minutes: 403 },
      { ts: '2025-11-09', steps: 4631, water_ml: 955, sleep_hours: 6.5, screen_minutes: 259 },
      { ts: '2025-11-10', steps: 7891, water_ml: 941, sleep_hours: 7.3, screen_minutes: 180 },
      { ts: '2025-11-11', steps: 1718, water_ml: 1260, sleep_hours: 6.6, screen_minutes: 296 },
      { ts: '2025-11-12', steps: 1081, water_ml: 928, sleep_hours: 8.1, screen_minutes: 134 },
      { ts: '2025-11-13', steps: 4089, water_ml: 852, sleep_hours: 8.2, screen_minutes: 285 },
      { ts: '2025-11-14', steps: 6354, water_ml: 1273, sleep_hours: 5.6, screen_minutes: 164 },
      { ts: '2025-11-15', steps: 8260, water_ml: 2268, sleep_hours: 5.9, screen_minutes: 182 },
      { ts: '2025-11-16', steps: 5816, water_ml: 1553, sleep_hours: 6.2, screen_minutes: 132 },
      { ts: '2025-11-17', steps: 4251, water_ml: 1503, sleep_hours: 4.6, screen_minutes: 204 },
      { ts: '2025-11-18', steps: 2289, water_ml: 1007, sleep_hours: 8.3, screen_minutes: 282 },
      { ts: '2025-11-19', steps: 1988, water_ml: 817, sleep_hours: 7.7, screen_minutes: 261 }
    ]
  }
};

export default function App() {
  const [data, setData] = useState(sampleData);
  const [userKey, setUserKey] = useState(Object.keys(sampleData)[0]);
  const [df, setDf] = useState(sampleData[userKey].telemetry);
  const [selectedIdx, setSelectedIdx] = useState(df.length - 1);

  useEffect(() => {
    setDf(data[userKey].telemetry);
  }, [data, userKey]);

  function toSeries(field) {
    return df.map((r) => (typeof r[field] === 'number' ? r[field] : 0));
  }

  function toLabels() {
    return df.map((r) => r.ts);
  }

  function computeHeuristics() {
    // hydration_flag, sleep_flag, low_activity
    const hydration_flag = df.map((r) => (r.water_ml < 1200 ? 1 : 0)).reduce((a, b) => a + b, 0);
    const sleep_flag = df.map((r) => (r.sleep_hours < 6 ? 1 : 0)).reduce((a, b) => a + b, 0);
    const low_activity = df.map((r) => (r.steps < 3000 ? 1 : 0)).reduce((a, b) => a + b, 0);
    return { hydration_flag, sleep_flag, low_activity };
  }

  async function pickFile() {
    const res = await DocumentPicker.getDocumentAsync({ type: 'application/json' });
    if (res.type === 'success') {
      const content = await FileSystem.readAsStringAsync(res.uri);
      try {
        const parsed = JSON.parse(content);
        setData(parsed);
        const key = Object.keys(parsed)[0];
        setUserKey(key);
        setSelectedIdx(parsed[key].telemetry.length - 1);
        alert('Loaded telemetry JSON');
      } catch (e) {
        alert('Invalid JSON');
      }
    }
  }

  const labels = toLabels();
  const stepsSeries = toSeries('steps');
  const waterSeries = toSeries('water_ml');
  const sleepSeries = toSeries('sleep_hours');
  const screenSeries = toSeries('screen_minutes');
  const heur = computeHeuristics();

  const latest = df[selectedIdx] || df[df.length - 1];

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={{ padding: 12 }}>
        <Text style={styles.title}>AutoHealth Guardian</Text>
        <View style={styles.metricsRow}>
          <View style={styles.card}>
            <Text style={styles.cardTitle}>Steps</Text>
            <Text style={styles.cardValue}>{latest.steps}</Text>
          </View>
          <View style={styles.card}>
            <Text style={styles.cardTitle}>Water (ml)</Text>
            <Text style={styles.cardValue}>{latest.water_ml}</Text>
          </View>
          <View style={styles.card}>
            <Text style={styles.cardTitle}>Sleep (hrs)</Text>
            <Text style={styles.cardValue}>{latest.sleep_hours}</Text>
          </View>
        </View>

        <Text style={styles.sectionTitle}>Hydration (ml)</Text>
        <LineChart
          data={{ labels: labels, datasets: [{ data: waterSeries }] }}
          width={screenWidth - 24}
          height={220}
          yAxisSuffix="ml"
          chartConfig={chartConfig}
          bezier
          style={styles.chart}
        />

        <Text style={styles.sectionTitle}>Steps</Text>
        <LineChart
          data={{ labels: labels, datasets: [{ data: stepsSeries }] }}
          width={screenWidth - 24}
          height={220}
          yAxisSuffix=""
          chartConfig={chartConfig}
          style={styles.chart}
        />

        <Text style={styles.sectionTitle}>Sleep (hours)</Text>
        <BarChart
          data={{ labels: labels, datasets: [{ data: sleepSeries }] }}
          width={screenWidth - 24}
          height={220}
          chartConfig={chartConfig}
          style={styles.chart}
        />

        <Text style={styles.sectionTitle}>Screen Minutes</Text>
        <LineChart
          data={{ labels: labels, datasets: [{ data: screenSeries }] }}
          width={screenWidth - 24}
          height={180}
          chartConfig={chartConfig}
          style={styles.chart}
        />

        <Text style={styles.sectionTitle}>Heuristics</Text>
        <View style={styles.heurRow}>
          <Text>Days low water: {heur.hydration_flag}</Text>
          <Text>Days low sleep: {heur.sleep_flag}</Text>
          <Text>Days low activity: {heur.low_activity}</Text>
        </View>

        <Text style={styles.sectionTitle}>Selected Day Detail</Text>
        <View style={styles.detailCard}>
          <Text>Date: {latest.ts}</Text>
          <Text>Steps: {latest.steps}</Text>
          <Text>Water (ml): {latest.water_ml}</Text>
          <Text>Sleep (hrs): {latest.sleep_hours}</Text>
          <Text>Screen (min): {latest.screen_minutes}</Text>
        </View>

        <TouchableOpacity style={styles.button} onPress={pickFile}>
          <Text style={styles.buttonText}>Upload telemetry JSON</Text>
        </TouchableOpacity>

      </ScrollView>
    </SafeAreaView>
  );
}

const chartConfig = {
  backgroundGradientFrom: '#fff',
  backgroundGradientTo: '#fff',
  color: (opacity = 1) => `rgba(33, 150, 243, ${opacity})`,
  labelColor: (opacity = 1) => `rgba(0,0,0,${opacity})`,
  strokeWidth: 2, // optional, default 3
  barPercentage: 0.5,
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f7f7f7' },
  title: { fontSize: 22, fontWeight: '700', marginBottom: 12 },
  metricsRow: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 12 },
  card: { backgroundColor: '#fff', padding: 12, borderRadius: 8, width: '32%', shadowColor: '#000', shadowOpacity: 0.05, shadowRadius: 4, elevation: 2 },
  cardTitle: { fontSize: 12, color: '#666' },
  cardValue: { fontSize: 18, fontWeight: '700', marginTop: 6 },
  sectionTitle: { fontSize: 16, fontWeight: '700', marginTop: 16, marginBottom: 8 },
  chart: { borderRadius: 8 },
  heurRow: { flexDirection: 'row', justifyContent: 'space-around', backgroundColor: '#fff', padding: 12, borderRadius: 8 },
  detailCard: { backgroundColor: '#fff', padding: 12, borderRadius: 8, marginBottom: 12 },
  button: { backgroundColor: '#2196F3', padding: 12, borderRadius: 8, alignItems: 'center', marginTop: 12 },
  buttonText: { color: '#fff', fontWeight: '700' }
});
