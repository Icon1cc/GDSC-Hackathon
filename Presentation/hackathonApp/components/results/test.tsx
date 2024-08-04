import {
  View,
  Text,
  StyleSheet,
  Pressable,
  Dimensions,
  FlatList,
} from "react-native";
import React, { useState, useEffect } from "react";

import Header from "../header";
import { Ionicons } from "@expo/vector-icons";

const windowWidth = Dimensions.get("window").width;

const DATA = [
  {
    question: "When did Thomas Edison died due to a heart attack?",
    answer1: "October 18, 1931",
    answer2: "November 18, 1931",
    answer3: "December 18, 1931",
  },
  {
    question: "Shallom my brothers",
    answer1: "This is the answer to the question.",
    answer2: "Alternative answer.",
    answer3: "This is the answer to the question.",
  },
  {
    question: "When did Hitler discover America?",
    answer1: "November 18, 1856",
    answer2: "Alternative answer.",
    answer3: "oeivoierjv",
  },
];

interface BulletProps {
  scroll: (x: number) => void;
  input: string;
}

interface RenderBulletProps {
  question: string;
  answer1: string;
  answer2: string;
  answer3: string;
  piece: number;
  setPiece: (x: number) => void;
}

const RenderBullet = ({
  question,
  answer1,
  answer2,
  answer3,
  piece,
  setPiece,
}: RenderBulletProps) => {
  const [valid1, setValid1] = useState(false);
  const [valid2, setValid2] = useState(false);
  const [valid3, setValid3] = useState(false);

  return (
    <View style={{ gap: 10 }}>
      <View style={styles.bullet}>
        <Text style={{ fontFamily: "niv-r-smallcaps", fontSize: 20 }}>
          {question}
        </Text>
      </View>
      <View style={{ paddingLeft: 80, gap: 10 }}>
        <Pressable
          onPress={() => setValid1(!valid1)}
          style={{ flexDirection: "row", alignItems: "center", gap: 10 }}
        >
          {valid1 ? (
            <Ionicons name="checkbox-outline" size={24} color="#314053" />
          ) : (
            <Ionicons name="square-outline" size={24} color="#314053" />
          )}

          <Text style={{ width: 225 }}>{answer1}</Text>
        </Pressable>
        <Pressable
          onPress={() => setValid2(!valid2)}
          style={{ flexDirection: "row", alignItems: "center", gap: 10 }}
        >
          {valid2 ? (
            <Ionicons name="checkbox-outline" size={24} color="#314053" />
          ) : (
            <Ionicons name="square-outline" size={24} color="#314053" />
          )}
          <Text style={{ width: 225 }}>{answer2}</Text>
        </Pressable>
        <Pressable
          onPress={() => setValid2(!valid3)}
          style={{ flexDirection: "row", alignItems: "center", gap: 10 }}
        >
          {valid3 ? (
            <Ionicons name="checkbox-outline" size={24} color="#314053" />
          ) : (
            <Ionicons name="square-outline" size={24} color="#314053" />
          )}
          <Text style={{ width: 225 }}>{answer3}</Text>
        </Pressable>
      </View>
    </View>
  );
};

const Test = ({ scroll, input }: BulletProps) => {
  const [active, setActive] = useState(false);
  const [piece, setPiece] = useState(0);
  const [data, setData] = useState(DATA);

  const scrollTo = () => {
    scroll(windowWidth * 2);
  };

  useEffect(() => {
    if (piece === DATA.length) {
      setActive(true);
    } else {
      setActive(false);
    }
  }, [piece]);

  useEffect(() => {
    const sendData = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/get-QA1/?query=${encodeURIComponent(input)}`,
          {
            method: "GET",
            headers: {
              Accept: "application/json",
            },
          }
        );
        const json = await response.json();
        console.log("problème", json.title1);

        setData([
          {
            question: json.title1,
            answer1: json.correct1,
            answer2: json.incorrect12,
            answer3: json.incorrect11,
          },
          {
            question: json.title2,
            answer1: json.correct2,
            answer2: json.incorrect21,
            answer3: json.incorrect22,
          },
          {
            question: json.title3,
            answer1: json.correct3,
            answer2: json.incorrect31,
            answer3: json.incorrect32,
          },
        ]);
      } catch (error) {
        console.error("Failed to fetch:", error);
      }
    };
    sendData();

    const timer = setTimeout(() => {
      setActive(true);
    }, 15000);
    return () => {
      clearTimeout(timer);
    };
  }, []);

  return (
    <View style={styles.container}>
      <Header
        title={"Test yourself!"}
        subtitle={
          "Answer correctly to all the following questions to skip to the next stage."
        }
      />
      <FlatList
        data={data}
        renderItem={({ item }) => (
          <RenderBullet
            question={item.question}
            answer1={item.answer1}
            answer2={item.answer2}
            answer3={item.answer3}
            piece={piece}
            setPiece={setPiece}
          />
        )}
        keyExtractor={(item, index) => index.toString()}
        ItemSeparatorComponent={() => <View style={{ height: 20 }} />}
        contentContainerStyle={styles.bulletContainer}
      />
      <Pressable
        onPress={scrollTo}
        disabled={!active}
        style={
          active
            ? styles.button
            : [styles.button, { backgroundColor: "#9AA3AA" }]
        }
      >
        <Text style={{ color: "white", fontSize: 24 }}>NEXT</Text>
      </Pressable>
    </View>
  );
};

export default Test;

const styles = StyleSheet.create({
  container: {
    width: windowWidth,
    padding: 15,
    flex: 1,
    gap: 40,
    justifyContent: "space-between",
  },
  button: {
    height: 60,
    borderRadius: 12,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#314053",
  },
  bulletContainer: {
    padding: 10,
    backgroundColor: "#E1E8EE",
    borderRadius: 12,
    gap: 10,
  },
  bullet: {
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
  },
});
