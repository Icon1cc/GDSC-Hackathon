import { Text, View, SafeAreaView, StyleSheet, Pressable } from "react-native";
import { Link } from "expo-router";
import React from "react";

import Header from "@/components/header";

const Home = () => {
  return (
    <SafeAreaView style={{ flex: 1, justifyContent: "center" }}>
      <View style={styles.container}>
        <Header
          title={"Welcome Back!"}
          subtitle={"Are you ready to learn something new?"}
        />
        <View style={{ gap: 15 }}>
          <Link href={"/insert-text"} asChild>
            <Pressable style={styles.button}>
              <Text
                style={{ color: "white", fontSize: 20, fontFamily: "niv-m" }}
              >
                Learn Something New
              </Text>
            </Pressable>
          </Link>
          <Link href={"/insert-pic"} asChild>
            <Pressable style={styles.button}>
              <Text
                style={{ color: "white", fontSize: 20, fontFamily: "niv-m" }}
              >
                Import New File
              </Text>
            </Pressable>
          </Link>
        </View>
      </View>
    </SafeAreaView>
  );
};

export default Home;

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: 15,
    gap: 50,
  },
  button: {
    height: 60,
    backgroundColor: "#314053",
    justifyContent: "center",
    alignItems: "center",
    padding: 15,
    borderRadius: 12,
  },
});
