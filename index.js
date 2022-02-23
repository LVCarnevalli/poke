const express = require("express")
const crypto = require("crypto")
const app = express()
const { Pool } = require("pg")
const bodyParser = require("body-parser")
var timeout = require("connect-timeout")
let port = process.env.PORT || 3000

app.use(timeout("5s"))
app.use(bodyParser.json())
app.use(haltOnTimedout)

function haltOnTimedout(req, res, next) {
    if (!req.timedout) next()
}

const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: {
        rejectUnauthorized: false,
    }
})

app.post("/user", async (req, res) => {
    const hex = crypto.randomBytes(50).toString("hex")
    const sql = `INSERT INTO public."user" (hash) VALUES ('${hex}')`
    await pool.query(sql)

    res.status(201).json({ hash: hex })
})

app.post("/poke", async (req, res) => {
    const body = req.body
    const sql = `INSERT INTO public."action" (from_hash,to_hash,operation) VALUES ('${body.from_hash}','${body.to_hash}','poke')`
    await pool.query(sql)

    res.sendStatus(204)
})

app.get("/action", async (req, res) => {
    const query = req.query
    let sql = `SELECT * FROM public."action" WHERE to_hash = '${query.to_hash}'`
    if (query.created_at) {
        sql += ` AND created_at > '${query.created_at}'`
    }
    const result = await pool.query(sql)

    res.json(result.rows)
})

app.listen(port, () => {
    console.log("server started...")
})