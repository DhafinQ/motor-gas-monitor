FROM nodered/node-red:5.0.4

WORKDIR /usr/src/node-red

COPY package.json /usr/src/node-red/package.json

RUN npm install --unsafe-perm

RUN node - <<'NODE'
const fs = require("fs");

const file = "/usr/src/node-red/node_modules/node-red-contrib-influxdb/influxdb.js";

let source = fs.readFileSync(file, "utf8");

const oldText =
`this.credentials.token;`;

const newText =
`this.credentials.token || process.env.INFLUX_TOKEN;`;

if (!source.includes(oldText)) {
    throw new Error("Could not find InfluxDB token expression");
}

source = source.replace(oldText, newText);

fs.writeFileSync(file, source);

console.log("InfluxDB node patched: credentials.token -> ENV fallback");
NODE

COPY settings.js /data/settings.js
COPY start.sh /start.sh

# ============================================================
# Patch node-red-node-email
# ============================================================
RUN node - <<'NODE'
const fs = require("fs");

const file =
  "/usr/src/node-red/node_modules/node-red-node-email/61-email.js";

let source = fs.readFileSync(file, "utf8");

const oldUserBlock =
/if\s*\(\s*this\.credentials\s*&&\s*this\.credentials\.hasOwnProperty\("userid"\)\s*\)\s*\{\s*this\.userid\s*=\s*this\.credentials\.userid;\s*\}\s*else\s+if\s*\(\s*this\.authtype\s*!==\s*"NONE"\s*\)\s*\{\s*this\.error\(RED\._\("email\.errors\.nouserid"\)\);\s*\}/s;

const newUserBlock = `
if (process.env.EMAIL_USER) {
    this.userid = process.env.EMAIL_USER;
}
else if (this.credentials && this.credentials.hasOwnProperty("userid")) {
    this.userid = this.credentials.userid;
}
else if (this.authtype !== "NONE") {
    this.error(RED._("email.errors.nouserid"));
}`;

if (!oldUserBlock.test(source)) {
    throw new Error(
        "Could not find node-red-node-email userid authentication block"
    );
}

source = source.replace(oldUserBlock, newUserBlock);


const oldPasswordBlock =
/if\s*\(\s*this\.authtype\s*===\s*"BASIC"\s*\)\s*\{\s*if\s*\(\s*this\.credentials\s*&&\s*this\.credentials\.hasOwnProperty\("password"\)\s*\)\s*\{\s*this\.password\s*=\s*this\.credentials\.password;\s*\}\s*else\s*\{\s*this\.error\(RED\._\("email\.errors\.nopassword"\)\);\s*\}\s*\}/s;

const newPasswordBlock = `
if (this.authtype === "BASIC") {
    if (process.env.EMAIL_PASS) {
        this.password = process.env.EMAIL_PASS;
    }
    else if (this.credentials && this.credentials.hasOwnProperty("password")) {
        this.password = this.credentials.password;
    }
    else {
        this.error(RED._("email.errors.nopassword"));
    }
}`;

if (!oldPasswordBlock.test(source)) {
    throw new Error(
        "Could not find node-red-node-email password authentication block"
    );
}

source = source.replace(oldPasswordBlock, newPasswordBlock);

fs.writeFileSync(file, source);

console.log(
    "Email node patched successfully:"
);
console.log(
    "  EMAIL_USER -> SMTP userid"
);
console.log(
    "  EMAIL_PASS -> SMTP password"
);
NODE

CMD ["/start.sh"]