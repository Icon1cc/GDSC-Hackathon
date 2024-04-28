import {
  View,
  Text,
  StyleSheet,
  Pressable,
  Dimensions,
  FlatList,
} from "react-native";
import React, { useEffect, useState } from "react";

import Header from "../header";
import { Octicons } from "@expo/vector-icons";

const windowWidth = Dimensions.get("window").width;

const DATA = [
  {
    title: "Here goes the bullet point title.",
    description:
      "You need to look more in detail about the pas tense of this sentece. Cum laude adas no papumus sacreum mea vida luda carnus lupus.",
  },
  {
    title: "Here goes the bullet point title.",
    description:
      "You need to look more in detail about the pas tense of this sentece. Cum laude adas no papumus sacreum mea vida luda carnus lupus.",
  },
  {
    title: "Here goes the bullet point title.",
    description:
      "You need to look more in detail about the pas tense of this sentece. Cum laude adas no papumus sacreum mea vida luda carnus lupus.",
  },
];

interface BulletProps {
  scroll: (x: number) => void;
  input: string;
}

interface RenderBulletProps {
  title: string;
  description: string;
  piece: number;
  setPiece: (x: number) => void;
}

const RenderBullet = ({
  title,
  description,
  piece,
  setPiece,
}: RenderBulletProps) => {
  const [show, setShow] = useState(false);

  useEffect(() => {
    if (show) {
      setPiece(piece + 1);
    } else if (!show && piece > 0) {
      setPiece(piece - 1);
    }
  }, [show]);

  return (
    <View style={{ gap: 10 }}>
      <Pressable style={styles.bullet} onPress={() => setShow(!show)}>
        <Octicons name="dot-fill" size={24} color="#314053" />
        <Text style={{ fontFamily: "niv-r-smallcaps", fontSize: 20 }}>
          {title}
        </Text>
      </Pressable>
      {show && <Text>{description}</Text>}
    </View>
  );
};

const Bullet = ({ scroll, input }: BulletProps) => {
  const [active, setActive] = useState(false);
  const [piece, setPiece] = useState(0);
  const [data, setData] = useState(DATA);

  const scrollTo = () => {
    scroll(windowWidth);
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
          `http://localhost:8000/get-bullet1/?query=${encodeURIComponent(
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

        setData([
          {
            title: json.title1,
            description: json.description1,
          },
          {
            title: json.title2,
            description: json.description2,
          },
          {
            title: json.title3,
            description: json.description3,
          },
        ]);
      } catch (error) {
        console.error("Failed to fetch:", error);
      }
    };
    sendData();
  }, []);

  console.log(data);

  return (
    <View style={styles.container}>
      <Header
        title={"Get Familiar!"}
        subtitle={"Train your knowledge with our curated propositions."}
      />
      <FlatList
        data={data ? data : DATA}
        renderItem={({ item }) => (
          <RenderBullet
            title={item.title}
            description={item.description}
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

export default Bullet;

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
