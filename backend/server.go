package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	firebase "firebase.google.com/go/v4"
	"firebase.google.com/go/v4/auth"
	"google.golang.org/api/option"

	"database/sql"

	_ "github.com/go-sql-driver/mysql"
)

type LoginRequest struct {
	UserID string `json:"usr_id"`
}

type QueryUploadRequest struct {
	UserID string `json:"usr_id"`
	Query  string `json:"query"`
}

type LLMRequest struct {
	UserID string `json:"usr_id"`
	Query  string `json:"query"`
}

// type DocumentListRequest struct {
// 	UserID string `json:"usr_id"`
// }

// type Document struct {
// 	ID          string `json:"id"`
// 	FileName    string `json:"file_name"`
// }

// func makeGetDocumentsHandler(db *sql.DB) http.HandlerFunc {
// 	return func(w http.ResponseWriter, r *http.Request) {
// 		// Allow requests from your frontend origin
// 		w.Header().Set("Access-Control-Allow-Origin", "http://localhost:5000")
// 		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
// 		w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")

// 		// Handle preflight request
// 		if r.Method == http.MethodOptions {
// 			w.WriteHeader(http.StatusOK)
// 			return
// 		}
// 		if r.Method != http.MethodPost {
// 			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
// 			return
// 		}
// 		var req DocumentListRequest
// 		if err := json.NewDecoder(r.Body).Decode(&req); err != nil || req.UserID== "" {
// 			http.Error(w, "Invalid JSON or missing token", http.StatusBadRequest)
// 			return
// 		}
// 		rows, err := db.Query(`
// 		SELECT id, user_id, file_name, storage_path, uploaded_at
// 		FROM documents
// 		WHERE user_id = $1`, req.UserID)
// 		if err != nil {
// 			http.Error(w, "DB query failed", http.StatusInternalServerError)
// 			log.Println("DB query error:", err)
// 			return
// 		}
// 		defer rows.Close()

// 		var documents []Document
// 		for rows.Next() {
// 			var doc Document
// 			if err := rows.Scan(&doc.ID, &doc.FileName); err != nil {
// 				http.Error(w, "Row scan failed", http.StatusInternalServerError)
// 				return
// 			}
// 			documents = append(documents, doc)
// 		}

// 		w.Header().Set("Content-Type", "application/json")
// 		json.NewEncoder(w).Encode(documents)
// 	}
// }

func makeLoginHandler(authClient *auth.Client, db *sql.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		// Allow requests from your frontend origin
		w.Header().Set("Access-Control-Allow-Origin", "http://localhost:5000")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
		w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")

		// Handle preflight request
		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusOK)
			return
		}
		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		var req LoginRequest
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil || req.UserID == "" {
			http.Error(w, "Invalid JSON or missing token", http.StatusBadRequest)
			return
		}
		token, err := authClient.VerifyIDToken(context.Background(), req.UserID)
		if err != nil {
			http.Error(w, "Invalid or expired token", http.StatusUnauthorized)
			return
		}

		fmt.Println("Login/UserID (Firebase UID):", token.UID)

		uid := token.UID
		email := token.Claims["email"].(string)

		_, err = db.Exec(`
    	    INSERT INTO users (id, email)
    	    VALUES (?, ?)
    	    ON DUPLICATE KEY UPDATE email = VALUES(email)`,
			uid, email,
		)
		if err != nil {
			http.Error(w, "Database connection error", http.StatusInternalServerError)
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]any{
			"success": true,
			"uid":     token.UID,
		})
	}
}

func main() {
	db, err := sql.Open("mysql", "root:NewPassw0rd!@tcp(localhost:3306)/user_db")
	if err != nil {
		log.Fatal("Failed to connect to DB:", err)
		return
	}
	defer db.Close()
	opt := option.WithCredentialsFile("docanpr-890f4-firebase-adminsdk-fbsvc-e554b19dce.json")
	app, err := firebase.NewApp(context.Background(), nil, opt)
	if err != nil {
		log.Fatalf("error initializing app: %v", err)
	}
	authClient, err := app.Auth(context.Background())
	if err != nil {
		log.Fatalf("error getting Auth client: %v", err)
		return
	}
	http.HandleFunc("/login", makeLoginHandler(authClient, db))
	// http.HandleFunc("/getDocuments", makeGetDocumentsHandler(db))

	fmt.Println("Server running on http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
