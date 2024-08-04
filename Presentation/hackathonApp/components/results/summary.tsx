import {
  View,
  Text,
  StyleSheet,
  Dimensions,
  Pressable,
  ScrollView,
} from "react-native";
import React, { useState, useEffect } from "react";

import Header from "../header";
import { Link } from "expo-router";

const windowWidth = Dimensions.get("window").width;

const DATA = {
  title: "Here goes the bullet point title.",
  description:
    "You need to look more in detail about the pas tense of this sentece. Cum laude adas no papumus sacreum mea vida luda carnus lupus.",
  part1: "Here goes the bullet point title.",
  part2: "You need to look more in detail about the pas tense of this sentece.",
  summary: "Cum laude adas no papumus sacreum mea vida luda carnus lupus.",
};

interface SummaryProps {
  input: string;
}

const Summary = ({ input }: SummaryProps) => {
  const [data, setData] = useState(DATA);

  useEffect(() => {
    const sendData = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/get-summary1/?query=${encodeURIComponent(
            input
          )}`,
          {
            method: "GET",
            headers: {
              Accept: "application/json",
            },
          }
        );
        const json = await response.json();
        console.log("problème", json.title1);

        setData({
          title: json.titleData,
          description: json.descriptionIdea,
          part1: json.part1,
          part2: json.part2,
          summary: json.summary,
        });
      } catch (error) {
        console.error("Failed to fetch:", error);
      }
    };
    sendData();
  }, []);
  return (
    <View style={styles.container}>
      <Header title="Let's recap!" subtitle="" />
      <ScrollView>
        <View style={styles.center}>
          <View>
            <Text style={{ fontSize: 28, fontFamily: "niv-b" }}>
              {data.title}
            </Text>
            <Text style={{ fontSize: 16, fontFamily: "niv-l" }}>
              {data.description}
            </Text>
          </View>

          <View style={{ gap: 5 }}>
            <Text style={{ fontSize: 18 }}>{data.part1}</Text>
            <Text style={{ fontSize: 18 }}>{data.part2}</Text>
          </View>

          <Text style={{ fontSize: 18 }}>{data.summary}</Text>
        </View>
      </ScrollView>
      <View style={styles.buttonContainer}>
        <Link href={"/"} asChild>
          <Pressable style={styles.button}>
            <Text style={{ color: "white", fontSize: 24 }}>HOME</Text>
          </Pressable>
        </Link>
        <Link href={"/"} asChild>
          <Pressable style={styles.button}>
            <Text style={{ color: "white", fontSize: 24 }}>MORE</Text>
          </Pressable>
        </Link>
      </View>
    </View>
  );
};

export default Summary;

const styles = StyleSheet.create({
  container: {
    width: windowWidth,
    padding: 15,
    flex: 1,
    gap: 40,
    justifyContent: "space-between",
  },
  center: {
    padding: 15,
    backgroundColor: "#E1E8EE",
    borderRadius: 12,
    gap: 40,
  },
  buttonContainer: {
    gap: 10,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  button: {
    height: 60,
    flex: 1,
    borderRadius: 12,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#314053",
  },
});
