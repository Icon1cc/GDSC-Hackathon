import {
  View,
  Text,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  Pressable,
  TextInput,
} from "react-native";
import { MaterialIcons } from "@expo/vector-icons";
import React, { useState } from "react";
import { Link } from "expo-router";

const CATEGORY = ["Science", "Math", "History", "Art", "Literature"];

const InsertText = () => {
  const [inputText, setInputText] = useState("");
  const [category, setCategory] = useState("Science");

  const handleCategory = (index: number) => {
    if (index < 0) index = CATEGORY.length - 1;
    else if (index >= CATEGORY.length) index = 0;
    setCategory(CATEGORY[index]);
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === "ios" ? "padding" : "height"}
      keyboardVerticalOffset={80}
      style={styles.container}
    >
      <View style={styles.caroussel}>
        <Pressable
          style={styles.arrow}
          onPress={() => handleCategory(CATEGORY.indexOf(category) - 1)}
        >
          <MaterialIcons name="arrow-back-ios-new" size={24} color="black" />
        </Pressable>
        <View
          style={{
            backgroundColor: "#314053",
            padding: 10,
            borderRadius: 12,
          }}
        >
          <Text style={{ color: "white", fontSize: 26 }}>{category}</Text>
        </View>
        <Pressable
          style={styles.arrow}
          onPress={() => handleCategory(CATEGORY.indexOf(category) + 1)}
        >
          <MaterialIcons name="arrow-forward-ios" size={24} color="black" />
        </Pressable>
      </View>
      <View style={{ gap: 5, flex: 1 }}>
        <Text style={{ fontSize: 24, paddingLeft: 5 }}>Add a question</Text>
        <TextInput
          placeholder="Add some information..."
          placeholderTextColor={"#314053"}
          onChangeText={(text) => setInputText(text)}
          value={inputText}
          style={styles.input}
        />
      </View>
      <Link
        href={{
          pathname: "/result/",
          params: { input: inputText },
        }}
        asChild
      >
        <Pressable style={styles.search}>
          <Text style={styles.searchText}>SEARCH</Text>
        </Pressable>
      </Link>
    </KeyboardAvoidingView>
  );
};

export default InsertText;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingVertical: 80,
    paddingHorizontal: 15,
    gap: 80,
  },
  caroussel: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 20,
  },
  arrow: {
    padding: 10,
    borderRadius: 15,
    backgroundColor: "#E1E8EE",
    justifyContent: "center",
    alignItems: "center",
  },
  search: {
    height: 50,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#314053",
    borderRadius: 12,
    marginBottom: 30,
  },
  searchText: {
    color: "white",
    fontSize: 24,
    fontFamily: "niv-r-smallcaps",
  },
  input: {
    height: 50,
    paddingHorizontal: 10,
    backgroundColor: "#E1E8EE",
    borderRadius: 12,
    fontSize: 18,
    fontFamily: "niv-r-smallcaps",
  },
});
