#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deterministic generator for data/aws_saa_pilot_DRAFT.json.

Module: aws_saa -- "AWS Certified Solutions Architect - Associate (SAA-C03)"

EN is the canonical locale (AWS publishes the exam guide and its service
documentation in English, and the exam itself is authored in English), with
DE, JA and ZH as parallel translations. This is the SAME minimal 4-locale set
the `cka` module shipped with on 2026-08-15 -- en/de/ja/zh, EN canonical --
and it is deliberately following that precedent rather than claiming a fresh
exception to AGENTS.md constraint 5. If the PO would rather have the full 12
locales for technical-certification modules, that is a one-line decision here
and a translation round; nothing in the schema below assumes four.

SOURCING (see docs/aws-saa-pre-review-dossier-2026-08-24.md):

  Tier A, and the only structural source: AWS's OWN public exam guide,
  "AWS Certified Solutions Architect - Associate (SAA-C03) Exam Guide",
  docs.aws.amazon.com/aws-certification/latest/solutions-architect-associate-03/
  retrieved 2026-08-24 in both HTML and PDF form. It supplies the exam code,
  the question counts (50 scored + 15 unscored = 65), the scaled passing score
  (720 of 100-1000), the four content domains, their percentage weightings,
  and the fourteen task statements. Those are FACTS about an examination, not
  expressive text; nothing from the guide is reproduced verbatim here beyond
  the domain and task-statement titles, which are functional headings.

  Tier A for every substantive answer: AWS's own public service documentation
  on docs.aws.amazon.com. Each question carries a `legal_basis` field naming
  the domain, the task statement, and the AWS documentation page the correct
  answer was verified against. Fifteen of those pages were fetched and read
  directly on 2026-08-24 (listed in meta.sources).

  NOT used as a source, directly or indirectly, at any point: any commercial
  exam-prep vendor's question text, explanations, wording or structure; any
  "dump" site; any paid AWS training course; any third-party book; AWS Skill
  Builder's own practice questions. AGENTS.md constraint 1 bans third-party
  exam-prep companies' text outright and there is no visual-accuracy carve-out
  that could apply to a question bank. Search results for this topic are
  dominated by such vendors; none was fetched.

  AWS EXAM CONTENT IS CONFIDENTIAL. The AWS Certification Agreement provides
  that "all Credential Assessment Materials are AWS Confidential Information"
  and forbids disclosing "the content of any Certification Exam". Nothing in
  this file is or purports to be real exam content. Every scenario, option and
  distractor below was authored from the public exam guide's task statements
  plus public AWS service documentation.

  TRADEMARKS. "AWS", "Amazon Web Services", "Amazon EC2", "Amazon S3" and the
  other service names used below are trademarks of Amazon.com, Inc. or its
  affiliates. They are used here nominatively, to name the services the exam
  is about, as AWS's own trademark guidelines contemplate ("AWS does not
  object to fair use of its marks by third parties, so long as the use would
  not be confusing for customers"). This module is NOT affiliated with,
  sponsored by, endorsed by or certified by AWS.

NOT wired into any build path. Not registered in build_modules.py or
modules_manifest.json. app/ untouched. Run manually:
    python3 data/gen_aws_saa_draft.py
The script performs its own integrity checks and exits non-zero on failure.
"""

import json
import os
import sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "aws_saa_pilot_DRAFT.json")

KEY_ORDER = ["id", "topic", "topic_code", "class_scope", "grundstoff",
             "legal_basis", "points", "high_stakes", "question_type",
             "image_ref", "correct", "text", "explanation"]

LOCALES = ["en", "de", "ja", "zh"]
LETTERS = "abcde"

# The four content domains of the SAA-C03 exam guide, with the exact
# weightings AWS publishes for each. The pilot's question distribution is
# checked against these at the bottom of this file.
DOMAINS = {
    "secure_architectures": {
        "weight": 30,
        "label": {
            "en": "Domain 1: Design Secure Architectures",
            "de": "Bereich 1: Sichere Architekturen entwerfen",
            "ja": "分野 1: セキュアなアーキテクチャの設計",
            "zh": "领域 1：设计安全的架构",
        },
    },
    "resilient_architectures": {
        "weight": 26,
        "label": {
            "en": "Domain 2: Design Resilient Architectures",
            "de": "Bereich 2: Ausfallsichere Architekturen entwerfen",
            "ja": "分野 2: 回復性の高いアーキテクチャの設計",
            "zh": "领域 2：设计弹性架构",
        },
    },
    "high_performing_architectures": {
        "weight": 24,
        "label": {
            "en": "Domain 3: Design High-Performing Architectures",
            "de": "Bereich 3: Leistungsstarke Architekturen entwerfen",
            "ja": "分野 3: 高性能アーキテクチャの設計",
            "zh": "领域 3：设计高性能架构",
        },
    },
    "cost_optimized_architectures": {
        "weight": 20,
        "label": {
            "en": "Domain 4: Design Cost-Optimized Architectures",
            "de": "Bereich 4: Kostenoptimierte Architekturen entwerfen",
            "ja": "分野 4: コスト最適化アーキテクチャの設計",
            "zh": "领域 4：设计成本优化的架构",
        },
    },
}

QUESTIONS = []


def Q(qid, topic_code, task, grundstoff, high_stakes, qtype, correct,
      verified_against, en, de, ja, zh):
    """Assemble one question object.

    en/de/ja/zh are each a 3-tuple: (question, [options...], explanation).
    `correct` is a list of option letters. Points follow the cka convention:
    1 point for fundamentals (`grundstoff`), 2 for the applied/scenario tier.
    """
    texts = {"en": en, "de": de, "ja": ja, "zh": zh}
    n_opts = len(en[1])
    text, explanation = {}, {}
    for loc in LOCALES:
        q, opts, expl = texts[loc]
        assert len(opts) == n_opts, "%s: %s option count differs" % (qid, loc)
        text[loc] = {
            "question": q,
            "options": {LETTERS[i]: opts[i] for i in range(n_opts)},
        }
        explanation[loc] = expl
    QUESTIONS.append({
        "id": qid,
        "topic": DOMAINS[topic_code]["label"]["en"],
        "topic_code": topic_code,
        "class_scope": ["ALL"],
        "grundstoff": grundstoff,
        "legal_basis": "SAA-C03 Exam Guide, %s | verified against %s"
                       % (task, verified_against),
        "points": 1 if grundstoff else 2,
        "high_stakes": high_stakes,
        "question_type": qtype,
        "image_ref": None,
        "correct": correct,
        "text": text,
        "explanation": explanation,
    })


SC = "single_choice"
MC = "multi_choice"

# =====================================================================
# Domain 1 - Design Secure Architectures (30% of scored content) - 11 Q
# =====================================================================

Q("aws-saa-secure-01", "secure_architectures",
  "Domain 1, Task Statement 1.1 (Design secure access to AWS resources)",
  True, True, SC, ["b"],
  "docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html",
  en=("An application running on Amazon EC2 instances must read objects from an Amazon S3 bucket. The current deployment stores long-lived IAM user access keys in a configuration file on each instance. Which change best follows AWS security best practices?",
      ["Move the access keys into an environment variable on each instance and rotate them manually every 90 days",
       "Attach an IAM role to the instances through an instance profile, scope its policy to the bucket, and delete the stored access keys",
       "Store the access keys in the S3 bucket itself and restrict the bucket policy to the instances' IP addresses",
       "Create one IAM user per instance and attach the AdministratorAccess managed policy to each"],
      "An IAM role attached through an instance profile delivers temporary credentials to the instance metadata service and rotates them automatically, so no long-lived secret is ever written to disk or baked into an AMI. Option a still stores a long-lived secret and depends on a manual process. Option c is circular (the credentials needed to read the bucket are inside the bucket) and an IP-based condition authenticates nothing. Option d violates least privilege in the most direct way possible."),
  de=("Eine Anwendung auf Amazon-EC2-Instanzen muss Objekte aus einem Amazon-S3-Bucket lesen. In der aktuellen Bereitstellung liegen langlebige Zugriffsschlüssel eines IAM-Benutzers in einer Konfigurationsdatei auf jeder Instanz. Welche Änderung entspricht den AWS-Sicherheitsempfehlungen am besten?",
      ["Die Zugriffsschlüssel in eine Umgebungsvariable auf jeder Instanz verschieben und alle 90 Tage manuell rotieren",
       "Den Instanzen über ein Instanzprofil eine IAM-Rolle zuweisen, deren Richtlinie auf den Bucket beschränken und die gespeicherten Zugriffsschlüssel löschen",
       "Die Zugriffsschlüssel im S3-Bucket selbst ablegen und die Bucket-Richtlinie auf die IP-Adressen der Instanzen beschränken",
       "Pro Instanz einen IAM-Benutzer anlegen und jedem die verwaltete Richtlinie AdministratorAccess zuweisen"],
      "Eine über ein Instanzprofil zugewiesene IAM-Rolle stellt der Instanz temporäre Anmeldeinformationen über den Instance Metadata Service bereit und rotiert sie automatisch. So landet kein langlebiges Geheimnis auf der Festplatte oder in einem AMI. Antwort a speichert weiterhin ein langlebiges Geheimnis und hängt an einem manuellen Prozess. Antwort c ist zirkulär (die Anmeldeinformationen zum Lesen des Buckets liegen im Bucket) und eine IP-Bedingung authentifiziert niemanden. Antwort d verletzt das Least-Privilege-Prinzip auf denkbar direkteste Weise."),
  ja=("Amazon EC2 インスタンス上で動作するアプリケーションが、Amazon S3 バケットからオブジェクトを読み取る必要があります。現在の構成では、長期間有効な IAM ユーザーのアクセスキーが各インスタンスの設定ファイルに保存されています。AWS のセキュリティのベストプラクティスに最も合致する変更はどれですか。",
      ["アクセスキーを各インスタンスの環境変数に移し、90 日ごとに手動でローテーションする",
       "インスタンスプロファイル経由で IAM ロールをインスタンスにアタッチし、そのポリシーを対象バケットに限定したうえで、保存済みのアクセスキーを削除する",
       "アクセスキーを S3 バケット自体に保存し、バケットポリシーをインスタンスの IP アドレスに制限する",
       "インスタンスごとに IAM ユーザーを作成し、それぞれに AdministratorAccess 管理ポリシーをアタッチする"],
      "インスタンスプロファイル経由でアタッチされた IAM ロールは、インスタンスメタデータサービスを通じて一時的な認証情報を配布し、自動的にローテーションします。そのため、長期間有効なシークレットがディスクや AMI に残ることはありません。選択肢 a は依然として長期シークレットを保存し、手動運用に依存します。選択肢 c は循環しており(バケットを読むための認証情報がバケット内にある)、IP 条件は認証にはなりません。選択肢 d は最小権限の原則を最も直接的に破ります。"),
  zh=("运行在 Amazon EC2 实例上的应用程序需要从 Amazon S3 存储桶读取对象。当前部署将长期有效的 IAM 用户访问密钥保存在每台实例的配置文件中。哪项变更最符合 AWS 安全最佳实践？",
      ["将访问密钥移入每台实例的环境变量，并每 90 天手动轮换一次",
       "通过实例配置文件为实例附加 IAM 角色，将其策略限定到该存储桶，并删除已保存的访问密钥",
       "把访问密钥存放在该 S3 存储桶中，并将存储桶策略限制为实例的 IP 地址",
       "为每台实例创建一个 IAM 用户，并为其附加 AdministratorAccess 托管策略"],
      "通过实例配置文件附加的 IAM 角色会经由实例元数据服务向实例下发临时凭证并自动轮换，因此不会有长期密钥写入磁盘或被打进 AMI。选项 a 仍然保存长期密钥，并依赖人工流程。选项 c 是循环依赖（读取存储桶所需的凭证放在存储桶里），而基于 IP 的条件并不构成身份验证。选项 d 以最直接的方式违反了最小权限原则。"))

Q("aws-saa-secure-02", "secure_architectures",
  "Domain 1, Task Statement 1.1 (Design secure access to AWS resources)",
  False, True, SC, ["c"],
  "docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html",
  en=("A company must let an external auditing firm read objects under one prefix of an S3 bucket from the auditor's own AWS account. Access must use short-lived credentials and must not involve handing over any secret. Which design should the solutions architect choose?",
      ["Create an IAM user in the company account, send the auditor its access keys, and scope the policy to the prefix",
       "Make the prefix publicly readable and send the auditor the object URLs",
       "Create an IAM role in the company account that trusts the auditor's account principal, scope its permissions to the prefix, and require an external ID when the role is assumed",
       "Configure S3 replication so the objects under that prefix are copied into a bucket owned by the auditor"],
      "Cross-account role assumption is the intended mechanism: the auditor calls sts:AssumeRole and receives credentials that expire, and the external ID protects against the confused-deputy problem where a third party persuades the auditor's account to use its trust on someone else's behalf. Option a hands over a long-lived secret. Option b exposes the data to everyone. Option d copies the data out of the company's control instead of granting scoped read access, and does not give the auditor a view of the live objects."),
  de=("Ein Unternehmen muss einer externen Wirtschaftsprüfungsgesellschaft erlauben, aus deren eigenem AWS-Konto Objekte unter einem Präfix eines S3-Buckets zu lesen. Der Zugriff muss mit kurzlebigen Anmeldeinformationen erfolgen und darf keine Weitergabe eines Geheimnisses erfordern. Welchen Entwurf sollte die Lösungsarchitektin wählen?",
      ["Einen IAM-Benutzer im Unternehmenskonto anlegen, dem Prüfer dessen Zugriffsschlüssel senden und die Richtlinie auf das Präfix beschränken",
       "Das Präfix öffentlich lesbar machen und dem Prüfer die Objekt-URLs senden",
       "Eine IAM-Rolle im Unternehmenskonto anlegen, die dem Prinzipal des Prüferkontos vertraut, ihre Berechtigungen auf das Präfix beschränken und beim Annehmen der Rolle eine External ID verlangen",
       "S3-Replikation so konfigurieren, dass die Objekte unter diesem Präfix in einen Bucket des Prüfers kopiert werden"],
      "Die kontenübergreifende Rollenübernahme ist der dafür vorgesehene Mechanismus: Der Prüfer ruft sts:AssumeRole auf und erhält ablaufende Anmeldeinformationen. Die External ID schützt vor dem Confused-Deputy-Problem, bei dem ein Dritter das Prüferkonto dazu bringt, sein Vertrauensverhältnis für jemand anderen einzusetzen. Antwort a gibt ein langlebiges Geheimnis heraus. Antwort b macht die Daten für jeden zugänglich. Antwort d kopiert die Daten aus dem Kontrollbereich des Unternehmens heraus, statt einen eng gefassten Lesezugriff zu gewähren, und zeigt dem Prüfer nicht die aktuellen Objekte."),
  ja=("ある企業は、外部監査法人が監査法人自身の AWS アカウントから、S3 バケットの特定のプレフィックス配下のオブジェクトを読み取れるようにする必要があります。アクセスは短期間の認証情報を用い、シークレットの受け渡しを伴ってはなりません。ソリューションアーキテクトが選ぶべき設計はどれですか。",
      ["企業アカウントに IAM ユーザーを作成し、そのアクセスキーを監査法人に送り、ポリシーをプレフィックスに限定する",
       "そのプレフィックスをパブリック読み取り可能にし、オブジェクト URL を監査法人に送る",
       "監査法人アカウントのプリンシパルを信頼する IAM ロールを企業アカウントに作成し、権限をプレフィックスに限定し、ロール引き受け時に外部 ID を要求する",
       "S3 レプリケーションを構成し、そのプレフィックス配下のオブジェクトを監査法人所有のバケットへコピーする"],
      "クロスアカウントのロール引き受けが本来の仕組みです。監査法人は sts:AssumeRole を呼び出して有効期限付きの認証情報を受け取ります。外部 ID は、第三者が監査法人アカウントの信頼関係を別の相手のために使わせる「混乱した代理人」問題を防ぎます。選択肢 a は長期シークレットを渡してしまいます。選択肢 b はデータを全世界に公開します。選択肢 d は限定的な読み取り権限を与える代わりにデータを企業の管理外へコピーするもので、監査法人に現行のオブジェクトを見せることにもなりません。"),
  zh=("某公司需要允许外部审计事务所从审计方自己的 AWS 账户读取某 S3 存储桶中一个前缀下的对象。访问必须使用短期凭证，且不得交出任何密钥。解决方案架构师应选择哪种设计？",
      ["在公司账户中创建一个 IAM 用户，把访问密钥发给审计方，并将策略限定到该前缀",
       "将该前缀设为公开可读，并把对象 URL 发给审计方",
       "在公司账户中创建一个信任审计方账户主体的 IAM 角色，将其权限限定到该前缀，并要求在担任角色时提供外部 ID",
       "配置 S3 复制，把该前缀下的对象复制到审计方拥有的存储桶中"],
      "跨账户担任角色正是为此设计的机制：审计方调用 sts:AssumeRole 获得会过期的凭证，而外部 ID 可防范“混淆代理人”问题，即第三方诱使审计方账户代表他人使用其信任关系。选项 a 交出了长期密钥。选项 b 把数据向所有人公开。选项 d 是把数据复制到公司控制范围之外，而不是授予受限的读取权限，并且审计方看到的也不是当前对象。"))

Q("aws-saa-secure-03", "secure_architectures",
  "Domain 1, Task Statement 1.1 (Design secure access to AWS resources)",
  True, True, SC, ["d"],
  "docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html",
  en=("What is the effect of attaching a service control policy (SCP) to an organizational unit in AWS Organizations?",
      ["It grants the listed permissions to every IAM principal in the member accounts of that OU",
       "It replaces the identity-based policies attached to IAM users and roles in those accounts",
       "It applies to the root user of the organization's management account in the same way as to member accounts",
       "It sets the maximum permissions available to IAM principals in those accounts, but grants nothing by itself"],
      "SCPs are guardrails, not grants. An action succeeds only if it is allowed by the applicable SCP AND by an identity-based or resource-based policy; an SCP on its own never lets anyone do anything. Identity-based policies are still required and are not replaced. SCPs also do not restrict principals in the management account, which is a common and dangerous misconception when designing a break-glass model."),
  de=("Welche Wirkung hat es, in AWS Organizations eine Service Control Policy (SCP) an eine Organisationseinheit anzuhängen?",
      ["Sie gewährt jedem IAM-Prinzipal in den Mitgliedskonten dieser OU die aufgeführten Berechtigungen",
       "Sie ersetzt die identitätsbasierten Richtlinien der IAM-Benutzer und -Rollen in diesen Konten",
       "Sie gilt für den Root-Benutzer des Verwaltungskontos der Organisation genauso wie für Mitgliedskonten",
       "Sie legt die maximal verfügbaren Berechtigungen für IAM-Prinzipale in diesen Konten fest, gewährt selbst aber nichts"],
      "SCPs sind Leitplanken, keine Berechtigungserteilungen. Eine Aktion gelingt nur, wenn sie sowohl von der wirksamen SCP als auch von einer identitäts- oder ressourcenbasierten Richtlinie erlaubt wird; eine SCP allein erlaubt niemandem irgendetwas. Identitätsbasierte Richtlinien bleiben erforderlich und werden nicht ersetzt. SCPs schränken zudem Prinzipale im Verwaltungskonto nicht ein - ein verbreiteter und gefährlicher Irrtum beim Entwurf eines Break-Glass-Modells."),
  ja=("AWS Organizations で組織単位 (OU) にサービスコントロールポリシー (SCP) をアタッチすると、どのような効果がありますか。",
      ["その OU 配下のメンバーアカウントのすべての IAM プリンシパルに、記載された権限を付与する",
       "それらのアカウントの IAM ユーザーやロールにアタッチされた ID ベースポリシーを置き換える",
       "組織の管理アカウントのルートユーザーにも、メンバーアカウントと同じように適用される",
       "それらのアカウントの IAM プリンシパルが利用できる権限の上限を定めるが、それ自体は何も付与しない"],
      "SCP は権限の付与ではなくガードレールです。アクションが成功するのは、有効な SCP と ID ベース(またはリソースベース)ポリシーの両方が許可している場合だけであり、SCP 単体では誰にも何も許可しません。ID ベースポリシーは依然として必要で、置き換えられることはありません。また SCP は管理アカウントのプリンシパルを制限しません。これはブレークグラス設計でよくある、そして危険な誤解です。"),
  zh=("在 AWS Organizations 中，将服务控制策略（SCP）附加到组织单位（OU）会产生什么效果？",
      ["为该 OU 下成员账户中的每个 IAM 主体授予所列出的权限",
       "取代这些账户中 IAM 用户和角色所附加的基于身份的策略",
       "对组织管理账户的根用户与对成员账户的作用方式相同",
       "设定这些账户中 IAM 主体可用权限的上限，但其本身不授予任何权限"],
      "SCP 是护栏，而不是授权。只有当生效的 SCP 与基于身份（或基于资源）的策略同时允许时，操作才会成功；单靠 SCP 永远不会让任何人获得权限。基于身份的策略仍然是必需的，不会被取代。此外，SCP 不会限制管理账户中的主体——这是设计应急访问（break-glass）模型时常见且危险的误解。"))

Q("aws-saa-secure-04", "secure_architectures",
  "Domain 1, Task Statement 1.2 (Design secure workloads and applications)",
  True, False, SC, ["a"],
  "docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html",
  en=("EC2 instances in private subnets must download objects from Amazon S3 in the same Region. Security requires that the traffic never traverse the public internet, and finance wants to avoid per-GB NAT gateway data-processing charges. What should the architect implement?",
      ["A gateway VPC endpoint for Amazon S3, with the endpoint route added to the private subnets' route tables",
       "An interface VPC endpoint (AWS PrivateLink) for Amazon S3 in every private subnet",
       "A NAT gateway in each Availability Zone with a default route to the internet gateway",
       "An AWS Direct Connect public virtual interface into the VPC"],
      "Gateway endpoints exist for exactly two services, Amazon S3 and DynamoDB. AWS states there is no additional charge for using them, and they work by adding a prefix-list route to the route tables you select, so S3 traffic stays on the AWS network. An interface endpoint for S3 also keeps traffic private but bills per endpoint-hour and per GB processed, so it fails the cost requirement. Option c is the arrangement being replaced. A Direct Connect public VIF is for connecting an on-premises network, not for keeping in-VPC traffic off the internet."),
  de=("EC2-Instanzen in privaten Subnetzen müssen Objekte aus Amazon S3 in derselben Region herunterladen. Die Sicherheitsabteilung verlangt, dass der Datenverkehr das öffentliche Internet nie berührt, und die Finanzabteilung will die Datenverarbeitungsgebühren pro GB am NAT-Gateway vermeiden. Was sollte umgesetzt werden?",
      ["Ein Gateway-VPC-Endpunkt für Amazon S3, dessen Route in die Routing-Tabellen der privaten Subnetze eingetragen wird",
       "Ein Interface-VPC-Endpunkt (AWS PrivateLink) für Amazon S3 in jedem privaten Subnetz",
       "Ein NAT-Gateway je Availability Zone mit einer Standardroute zum Internet-Gateway",
       "Ein AWS-Direct-Connect-Public-Virtual-Interface in die VPC"],
      "Gateway-Endpunkte gibt es für genau zwei Dienste: Amazon S3 und DynamoDB. Laut AWS fallen für ihre Nutzung keine zusätzlichen Gebühren an; sie funktionieren, indem eine Präfixlisten-Route in die ausgewählten Routing-Tabellen eingetragen wird, sodass der S3-Verkehr im AWS-Netz bleibt. Ein Interface-Endpunkt für S3 hält den Verkehr ebenfalls privat, wird aber pro Endpunktstunde und pro verarbeitetem GB abgerechnet und erfüllt die Kostenanforderung damit nicht. Antwort c ist genau die Konstruktion, die ersetzt werden soll. Ein Direct-Connect-Public-VIF verbindet ein lokales Rechenzentrum und hat mit VPC-internem Verkehr nichts zu tun."),
  ja=("プライベートサブネット内の EC2 インスタンスが、同一リージョンの Amazon S3 からオブジェクトをダウンロードする必要があります。セキュリティ要件として通信がパブリックインターネットを経由してはならず、コスト面では NAT ゲートウェイの GB 単位のデータ処理料金を避けたいと考えています。何を実装すべきですか。",
      ["Amazon S3 用のゲートウェイ VPC エンドポイントを作成し、そのルートをプライベートサブネットのルートテーブルに追加する",
       "各プライベートサブネットに Amazon S3 用のインターフェイス VPC エンドポイント (AWS PrivateLink) を作成する",
       "各アベイラビリティーゾーンに NAT ゲートウェイを配置し、インターネットゲートウェイへのデフォルトルートを設定する",
       "VPC への AWS Direct Connect パブリック仮想インターフェイスを構成する"],
      "ゲートウェイエンドポイントが利用できるのは Amazon S3 と DynamoDB のちょうど 2 サービスだけです。AWS はその利用に追加料金はかからないと明記しており、選択したルートテーブルにプレフィックスリスト宛のルートを追加することで動作するため、S3 宛の通信は AWS ネットワーク内に留まります。S3 のインターフェイスエンドポイントも通信を非公開に保ちますが、エンドポイント時間単位と処理 GB 単位で課金されるため、コスト要件を満たしません。選択肢 c は置き換えようとしている構成そのものです。Direct Connect のパブリック VIF はオンプレミス接続のためのもので、VPC 内通信の話ではありません。"),
  zh=("私有子网中的 EC2 实例需要从同一区域的 Amazon S3 下载对象。安全部门要求流量绝不能经过公共互联网，财务部门希望避免 NAT 网关按 GB 计费的数据处理费用。架构师应实施什么？",
      ["为 Amazon S3 创建网关 VPC 终端节点，并将其路由添加到私有子网的路由表中",
       "在每个私有子网中为 Amazon S3 创建接口 VPC 终端节点（AWS PrivateLink）",
       "在每个可用区部署 NAT 网关，并配置指向互联网网关的默认路由",
       "为该 VPC 配置 AWS Direct Connect 公有虚拟接口"],
      "网关终端节点恰好只支持两种服务：Amazon S3 和 DynamoDB。AWS 明确说明使用网关终端节点不收取额外费用；其工作方式是向所选路由表中添加一条指向前缀列表的路由，因此 S3 流量始终留在 AWS 网络内。S3 的接口终端节点同样能保持流量私有，但按终端节点小时和处理的 GB 计费，因此不满足成本要求。选项 c 正是要被替换掉的方案。Direct Connect 公有虚拟接口用于连接本地数据中心，与 VPC 内部流量无关。"))

Q("aws-saa-secure-05", "secure_architectures",
  "Domain 1, Task Statement 1.2 (Design secure workloads and applications)",
  False, True, SC, ["c"],
  "docs.aws.amazon.com/vpc/latest/userguide/infrastructure-security.html",
  en=("A single external IP address is repeatedly probing an application. The team wants to block just that source address for every instance in a subnet, leaving all other traffic unchanged. Which control should be used, and why?",
      ["A security group inbound rule that denies the address, because security groups are evaluated before network ACLs",
       "A route table entry that blackholes the address, because route tables are evaluated per instance",
       "A network ACL deny rule on the subnet, because network ACLs support explicit deny rules and security groups do not",
       "A security group outbound rule that denies the address, because security group return traffic is stateless"],
      "AWS's own comparison is unambiguous: security groups support allow rules only, are stateful, evaluate all rules before deciding, and operate at instance level. Network ACLs support allow AND deny, are stateless, are evaluated in ascending rule order until a match, and operate at subnet level. Blocking one source for a whole subnet is therefore a network ACL job. A route table cannot express this at all: routes are chosen by destination, not source, so there is nothing to blackhole for an inbound probe."),
  de=("Eine einzelne externe IP-Adresse scannt wiederholt eine Anwendung. Das Team möchte genau diese Quelladresse für alle Instanzen eines Subnetzes blockieren und den übrigen Verkehr unverändert lassen. Welches Mittel ist richtig, und warum?",
      ["Eine eingehende Security-Group-Regel, die die Adresse verweigert, weil Security Groups vor Netzwerk-ACLs ausgewertet werden",
       "Ein Routing-Tabelleneintrag, der die Adresse in ein Blackhole leitet, weil Routing-Tabellen pro Instanz ausgewertet werden",
       "Eine Deny-Regel in der Netzwerk-ACL des Subnetzes, weil Netzwerk-ACLs ausdrückliche Deny-Regeln unterstützen und Security Groups nicht",
       "Eine ausgehende Security-Group-Regel, die die Adresse verweigert, weil der Rückverkehr bei Security Groups zustandslos ist"],
      "Die Gegenüberstellung von AWS ist eindeutig: Security Groups kennen nur Allow-Regeln, sind zustandsbehaftet, werten alle Regeln aus, bevor sie entscheiden, und wirken auf Instanzebene. Netzwerk-ACLs kennen Allow UND Deny, sind zustandslos, werden in aufsteigender Regelnummer bis zum ersten Treffer ausgewertet und wirken auf Subnetzebene. Das Sperren einer Quelle für ein ganzes Subnetz ist damit Aufgabe einer Netzwerk-ACL. Eine Routing-Tabelle kann das gar nicht ausdrücken: Routen werden nach Ziel gewählt, nicht nach Quelle."),
  ja=("特定の外部 IP アドレス 1 つが、アプリケーションを繰り返しスキャンしています。チームは、その送信元アドレスだけをサブネット内のすべてのインスタンスに対して遮断し、他の通信には影響を与えたくないと考えています。どの制御を使うべきで、その理由は何ですか。",
      ["セキュリティグループのインバウンド拒否ルール。セキュリティグループはネットワーク ACL より先に評価されるため",
       "ルートテーブルで当該アドレスをブラックホールに向けるエントリ。ルートテーブルはインスタンスごとに評価されるため",
       "サブネットのネットワーク ACL の拒否ルール。ネットワーク ACL は明示的な拒否ルールをサポートし、セキュリティグループはサポートしないため",
       "セキュリティグループのアウトバウンド拒否ルール。セキュリティグループの戻りトラフィックはステートレスであるため"],
      "AWS 自身の比較表は明確です。セキュリティグループは許可ルールのみをサポートし、ステートフルで、すべてのルールを評価してから判断し、インスタンスレベルで動作します。ネットワーク ACL は許可と拒否の両方をサポートし、ステートレスで、ルール番号の昇順に最初に一致するまで評価され、サブネットレベルで動作します。したがって、サブネット全体に対して 1 つの送信元を遮断するのはネットワーク ACL の役割です。ルートテーブルではそもそも表現できません。ルートは送信元ではなく宛先で選ばれるからです。"),
  zh=("某个外部 IP 地址正在反复探测一个应用程序。团队希望仅针对该源地址、对某子网内所有实例进行阻断，同时不影响其他流量。应使用哪种控制手段，为什么？",
      ["安全组入站拒绝规则，因为安全组先于网络 ACL 被评估",
       "在路由表中把该地址导向黑洞的条目，因为路由表是按实例评估的",
       "在该子网的网络 ACL 上添加拒绝规则，因为网络 ACL 支持显式拒绝规则而安全组不支持",
       "安全组出站拒绝规则，因为安全组的返回流量是无状态的"],
      "AWS 自己的对比表述非常明确：安全组只支持允许规则，是有状态的，会在决定前评估所有规则，作用于实例级别；网络 ACL 同时支持允许和拒绝规则，是无状态的，按规则编号升序评估直到匹配，作用于子网级别。因此，针对整个子网阻断某一个源地址属于网络 ACL 的职责。路由表根本无法表达这一需求：路由是按目的地而非来源选择的。"))

Q("aws-saa-secure-06", "secure_architectures",
  "Domain 1, Task Statement 1.2 (Design secure workloads and applications)",
  True, True, SC, ["b"],
  "docs.aws.amazon.com/waf/latest/developerguide/what-is-aws-waf.html and docs.aws.amazon.com/waf/latest/developerguide/ddos-advanced-summary.html",
  en=("A public web application behind an Application Load Balancer is receiving both SQL injection attempts in HTTP request bodies and a large volumetric network flood. Which combination addresses both, at the right layer for each?",
      ["Amazon GuardDuty for the injection attempts and AWS WAF for the flood",
       "AWS WAF with a managed rule group for the injection attempts and AWS Shield Advanced for the volumetric flood",
       "Network ACLs for the injection attempts and security groups for the flood",
       "Amazon Inspector for the injection attempts and Amazon Macie for the flood"],
      "AWS WAF inspects HTTP(S) requests at layer 7 and ships AWS managed rule groups for SQL injection and cross-site scripting; it can be attached to an ALB, CloudFront or API Gateway. AWS Shield Advanced adds layer 3/4 DDoS detection and mitigation, 24/7 response-team access and cost protection. GuardDuty is a threat-detection service, Inspector is vulnerability assessment and Macie is sensitive-data discovery: all three report, none of them blocks traffic. Network ACLs and security groups cannot read an HTTP body."),
  de=("Eine öffentliche Webanwendung hinter einem Application Load Balancer erhält sowohl SQL-Injection-Versuche in HTTP-Anfragekörpern als auch eine große volumetrische Netzwerkflut. Welche Kombination adressiert beides auf der jeweils richtigen Ebene?",
      ["Amazon GuardDuty für die Injection-Versuche und AWS WAF für die Flut",
       "AWS WAF mit einer verwalteten Regelgruppe für die Injection-Versuche und AWS Shield Advanced für die volumetrische Flut",
       "Netzwerk-ACLs für die Injection-Versuche und Security Groups für die Flut",
       "Amazon Inspector für die Injection-Versuche und Amazon Macie für die Flut"],
      "AWS WAF prüft HTTP(S)-Anfragen auf Schicht 7 und liefert von AWS verwaltete Regelgruppen für SQL Injection und Cross-Site-Scripting; es lässt sich an ALB, CloudFront oder API Gateway hängen. AWS Shield Advanced ergänzt Erkennung und Abwehr von DDoS auf Schicht 3/4, Zugang zum Response-Team rund um die Uhr sowie Kostenschutz. GuardDuty ist Bedrohungserkennung, Inspector ist Schwachstellenbewertung und Macie ist Erkennung sensibler Daten: Alle drei melden, keines blockiert Verkehr. Netzwerk-ACLs und Security Groups können keinen HTTP-Body lesen."),
  ja=("Application Load Balancer の背後にある公開ウェブアプリケーションが、HTTP リクエストボディ内の SQL インジェクション試行と、大規模なボリューム型ネットワーク攻撃の両方を受けています。それぞれ適切なレイヤーで対処する組み合わせはどれですか。",
      ["インジェクション試行には Amazon GuardDuty、フラッドには AWS WAF",
       "インジェクション試行にはマネージドルールグループを使った AWS WAF、ボリューム型フラッドには AWS Shield Advanced",
       "インジェクション試行にはネットワーク ACL、フラッドにはセキュリティグループ",
       "インジェクション試行には Amazon Inspector、フラッドには Amazon Macie"],
      "AWS WAF はレイヤー 7 で HTTP(S) リクエストを検査し、SQL インジェクションやクロスサイトスクリプティング向けの AWS マネージドルールグループを提供します。ALB、CloudFront、API Gateway にアタッチできます。AWS Shield Advanced はレイヤー 3/4 の DDoS 検出と緩和、24 時間 365 日の対応チームへのアクセス、コスト保護を追加します。GuardDuty は脅威検出、Inspector は脆弱性評価、Macie は機微データの検出であり、いずれも検知・報告はしても通信を遮断しません。ネットワーク ACL とセキュリティグループは HTTP ボディを読めません。"),
  zh=("位于 Application Load Balancer 之后的公开 Web 应用同时遭遇 HTTP 请求体中的 SQL 注入尝试和大规模流量型网络洪水攻击。哪种组合能在各自恰当的层面同时应对两者？",
      ["用 Amazon GuardDuty 应对注入尝试，用 AWS WAF 应对洪水攻击",
       "用带托管规则组的 AWS WAF 应对注入尝试，用 AWS Shield Advanced 应对流量型洪水攻击",
       "用网络 ACL 应对注入尝试，用安全组应对洪水攻击",
       "用 Amazon Inspector 应对注入尝试，用 Amazon Macie 应对洪水攻击"],
      "AWS WAF 在第 7 层检查 HTTP(S) 请求，并提供针对 SQL 注入和跨站脚本的 AWS 托管规则组，可附加到 ALB、CloudFront 或 API Gateway。AWS Shield Advanced 增加第 3/4 层 DDoS 检测与缓解、7×24 响应团队支持以及费用保护。GuardDuty 是威胁检测，Inspector 是漏洞评估，Macie 是敏感数据发现：三者都只负责发现和报告，都不会阻断流量。网络 ACL 和安全组无法读取 HTTP 请求体。"))

Q("aws-saa-secure-07", "secure_architectures",
  "Domain 1, Task Statement 1.3 (Determine appropriate data security controls)",
  False, True, SC, ["d"],
  "docs.aws.amazon.com/kms/latest/developerguide/concepts.html and docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html",
  en=("Objects in an S3 bucket must be encrypted at rest with a key the company itself controls, every use of that key must appear in an audit trail, and the company must be able to disable the key immediately so that no further decryption is possible. Which option meets all three requirements?",
      ["Server-side encryption with Amazon S3 managed keys (SSE-S3)",
       "Server-side encryption with the AWS managed key aws/s3 (SSE-KMS)",
       "Client-side encryption with the data key stored as an object in the same bucket",
       "Server-side encryption with a customer managed AWS KMS key (SSE-KMS)"],
      "Only a customer managed KMS key gives the customer all three: an editable key policy, CloudTrail entries for every Encrypt, Decrypt and GenerateDataKey call, and the ability to disable the key or schedule its deletion, which immediately stops decryption of everything it protects. SSE-S3 exposes no key controls at all. The AWS managed aws/s3 key cannot be disabled or have its policy edited by the customer. Storing the data key next to the ciphertext defeats the entire purpose of encrypting."),
  de=("Objekte in einem S3-Bucket müssen im Ruhezustand mit einem Schlüssel verschlüsselt werden, den das Unternehmen selbst kontrolliert. Jede Verwendung dieses Schlüssels muss in einem Prüfpfad erscheinen, und das Unternehmen muss den Schlüssel sofort deaktivieren können, sodass keine weitere Entschlüsselung möglich ist. Welche Option erfüllt alle drei Anforderungen?",
      ["Serverseitige Verschlüsselung mit von Amazon S3 verwalteten Schlüsseln (SSE-S3)",
       "Serverseitige Verschlüsselung mit dem von AWS verwalteten Schlüssel aws/s3 (SSE-KMS)",
       "Clientseitige Verschlüsselung, wobei der Datenschlüssel als Objekt im selben Bucket liegt",
       "Serverseitige Verschlüsselung mit einem kundenverwalteten AWS-KMS-Schlüssel (SSE-KMS)"],
      "Nur ein kundenverwalteter KMS-Schlüssel liefert alle drei Punkte: eine bearbeitbare Schlüsselrichtlinie, CloudTrail-Einträge für jeden Aufruf von Encrypt, Decrypt und GenerateDataKey sowie die Möglichkeit, den Schlüssel zu deaktivieren oder seine Löschung zu planen, was die Entschlüsselung aller damit geschützten Daten sofort beendet. SSE-S3 bietet überhaupt keine Schlüsselsteuerung. Der von AWS verwaltete Schlüssel aws/s3 kann vom Kunden weder deaktiviert noch in seiner Richtlinie geändert werden. Den Datenschlüssel neben dem Chiffrat abzulegen, hebt den Zweck der Verschlüsselung auf."),
  ja=("S3 バケット内のオブジェクトは、企業自身が管理する鍵で保存時に暗号化されなければならず、その鍵の利用はすべて監査証跡に残る必要があり、さらに企業は鍵を即座に無効化してそれ以上の復号を不可能にできなければなりません。3 つの要件をすべて満たすのはどれですか。",
      ["Amazon S3 マネージドキーによるサーバー側暗号化 (SSE-S3)",
       "AWS マネージドキー aws/s3 によるサーバー側暗号化 (SSE-KMS)",
       "同じバケット内にオブジェクトとしてデータキーを保存するクライアント側暗号化",
       "カスタマーマネージド AWS KMS キーによるサーバー側暗号化 (SSE-KMS)"],
      "3 つすべてを満たすのはカスタマーマネージド KMS キーだけです。編集可能なキーポリシー、Encrypt・Decrypt・GenerateDataKey の各呼び出しに対する CloudTrail 記録、そして鍵の無効化や削除のスケジュール(これによりその鍵で保護されたすべてのデータの復号が直ちに止まる)が得られます。SSE-S3 には鍵の制御手段が一切ありません。AWS マネージドキー aws/s3 は顧客が無効化することもポリシーを編集することもできません。データキーを暗号文の隣に置く方式は、暗号化の目的そのものを損ないます。"),
  zh=("S3 存储桶中的对象必须使用公司自己控制的密钥进行静态加密，该密钥的每次使用都必须出现在审计记录中，并且公司必须能够立即禁用该密钥，从而阻止任何进一步的解密。哪一项能同时满足这三项要求？",
      ["使用 Amazon S3 托管密钥的服务器端加密（SSE-S3）",
       "使用 AWS 托管密钥 aws/s3 的服务器端加密（SSE-KMS）",
       "客户端加密，并把数据密钥作为对象存放在同一个存储桶中",
       "使用客户托管 AWS KMS 密钥的服务器端加密（SSE-KMS）"],
      "只有客户托管的 KMS 密钥能同时提供这三点：可编辑的密钥策略、对每次 Encrypt/Decrypt/GenerateDataKey 调用的 CloudTrail 记录，以及禁用密钥或安排删除的能力——一旦禁用，该密钥保护的所有数据将立即无法解密。SSE-S3 完全不提供密钥控制。AWS 托管密钥 aws/s3 无法由客户禁用，其策略也不可由客户编辑。把数据密钥与密文放在一起完全违背了加密的初衷。"))

Q("aws-saa-secure-08", "secure_architectures",
  "Domain 1, Task Statement 1.3 (Determine appropriate data security controls)",
  True, False, SC, ["a"],
  "docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html",
  en=("An application needs database credentials that are rotated automatically on a schedule, with the rotation actually performed against the database so the old credential stops working. Which service is purpose-built for this?",
      ["AWS Secrets Manager",
       "AWS Systems Manager Parameter Store standard parameters",
       "AWS Key Management Service (AWS KMS)",
       "Amazon S3 with default encryption enabled"],
      "Secrets Manager provides managed rotation: a rotation Lambda function changes the credential in the target database and updates the stored secret in the same workflow, and it ships ready-made rotation functions for the supported RDS engines. Parameter Store can hold an encrypted SecureString and is cheaper, but it does not rotate the credential inside the database. KMS manages encryption keys, not application credentials. An encrypted S3 object is just storage with no rotation logic at all."),
  de=("Eine Anwendung benötigt Datenbank-Anmeldeinformationen, die planmäßig automatisch rotiert werden, wobei die Rotation tatsächlich gegen die Datenbank ausgeführt wird, sodass die alten Anmeldeinformationen ungültig werden. Welcher Dienst ist genau dafür gebaut?",
      ["AWS Secrets Manager",
       "Standardparameter im AWS Systems Manager Parameter Store",
       "AWS Key Management Service (AWS KMS)",
       "Amazon S3 mit aktivierter Standardverschlüsselung"],
      "Secrets Manager bietet verwaltete Rotation: Eine Rotations-Lambda-Funktion ändert die Anmeldeinformationen in der Zieldatenbank und aktualisiert im selben Ablauf das gespeicherte Secret; für die unterstützten RDS-Engines liefert AWS fertige Rotationsfunktionen mit. Der Parameter Store kann einen verschlüsselten SecureString halten und ist günstiger, rotiert die Anmeldeinformationen in der Datenbank aber nicht. KMS verwaltet Verschlüsselungsschlüssel, keine Anwendungsanmeldeinformationen. Ein verschlüsseltes S3-Objekt ist reiner Speicher ohne jede Rotationslogik."),
  ja=("アプリケーションは、スケジュールに従って自動的にローテーションされるデータベース認証情報を必要としています。ローテーションは実際にデータベースに対して実行され、古い認証情報が使えなくなる必要があります。この用途のために作られたサービスはどれですか。",
      ["AWS Secrets Manager",
       "AWS Systems Manager Parameter Store の標準パラメータ",
       "AWS Key Management Service (AWS KMS)",
       "デフォルト暗号化を有効にした Amazon S3"],
      "Secrets Manager はマネージドローテーションを提供します。ローテーション用 Lambda 関数が対象データベース内の認証情報を変更し、同じワークフローで保存済みシークレットを更新します。サポート対象の RDS エンジン向けには既製のローテーション関数も用意されています。Parameter Store は暗号化された SecureString を保持でき、コストも低いですが、データベース内の認証情報自体をローテーションはしません。KMS が管理するのは暗号鍵であって、アプリケーションの認証情報ではありません。暗号化された S3 オブジェクトは単なるストレージであり、ローテーションのロジックは一切ありません。"),
  zh=("某应用需要按计划自动轮换的数据库凭证，并且轮换必须实际在数据库上执行，使旧凭证失效。哪项服务是专为此设计的？",
      ["AWS Secrets Manager",
       "AWS Systems Manager Parameter Store 标准参数",
       "AWS Key Management Service（AWS KMS）",
       "启用了默认加密的 Amazon S3"],
      "Secrets Manager 提供托管轮换：轮换 Lambda 函数会在目标数据库中更改凭证，并在同一流程中更新所存储的密钥值；对于受支持的 RDS 引擎，AWS 还提供现成的轮换函数。Parameter Store 可以保存加密的 SecureString 且更便宜，但它不会轮换数据库内部的凭证。KMS 管理的是加密密钥，而不是应用凭证。加密的 S3 对象只是存储，完全没有轮换逻辑。"))

Q("aws-saa-secure-09", "secure_architectures",
  "Domain 1, Task Statement 1.2 (Design secure workloads and applications)",
  False, True, MC, ["a", "b"],
  "docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html",
  en=("A static website is served by Amazon CloudFront with an Amazon S3 bucket as the origin. Visitors must not be able to reach the objects through their S3 URLs. Which TWO actions together achieve this?",
      ["Enable S3 Block Public Access on the bucket and remove any public-read bucket policy or ACL",
       "Attach an origin access control (OAC) to the CloudFront origin and add a bucket policy that allows s3:GetObject only to that CloudFront distribution",
       "Configure the bucket as an S3 static website endpoint and restrict it with a network ACL",
       "Move the bucket into a private subnet of the VPC",
       "Enable S3 Requester Pays on the bucket"],
      "Origin access control lets CloudFront sign its requests to S3 with SigV4; the bucket policy then grants s3:GetObject to the CloudFront service principal with an aws:SourceArn condition naming the distribution, so no other caller succeeds. Block Public Access ensures no leftover public ACL or policy re-opens the bucket behind your back. Option c is self-defeating, because the S3 website endpoint is public by design and network ACLs do not apply to S3 at all. Option d is impossible: S3 is a regional service, not a VPC resource, and has no subnet. Option e changes who pays for requests, not who may make them."),
  de=("Eine statische Website wird über Amazon CloudFront mit einem Amazon-S3-Bucket als Ursprung ausgeliefert. Besucher dürfen die Objekte nicht über ihre S3-URLs erreichen können. Welche ZWEI Maßnahmen erreichen das zusammen?",
      ["S3 Block Public Access für den Bucket aktivieren und alle öffentlichen Lese-Bucket-Richtlinien oder ACLs entfernen",
       "Eine Origin Access Control (OAC) an den CloudFront-Ursprung hängen und eine Bucket-Richtlinie hinzufügen, die s3:GetObject nur dieser CloudFront-Distribution erlaubt",
       "Den Bucket als statischen S3-Website-Endpunkt konfigurieren und ihn mit einer Netzwerk-ACL einschränken",
       "Den Bucket in ein privates Subnetz der VPC verschieben",
       "S3 Requester Pays für den Bucket aktivieren"],
      "Origin Access Control lässt CloudFront seine Anfragen an S3 mit SigV4 signieren; die Bucket-Richtlinie gewährt s3:GetObject dann nur dem CloudFront-Service-Prinzipal mit einer aws:SourceArn-Bedingung auf die Distribution, sodass kein anderer Aufrufer durchkommt. Block Public Access stellt sicher, dass keine übrig gebliebene öffentliche ACL oder Richtlinie den Bucket hintenherum wieder öffnet. Antwort c ist widersinnig, weil der S3-Website-Endpunkt konstruktionsbedingt öffentlich ist und Netzwerk-ACLs auf S3 überhaupt nicht wirken. Antwort d ist unmöglich: S3 ist ein regionaler Dienst, keine VPC-Ressource, und hat kein Subnetz. Antwort e ändert, wer für Anfragen zahlt, nicht, wer sie stellen darf."),
  ja=("静的ウェブサイトを Amazon CloudFront で配信し、オリジンとして Amazon S3 バケットを使用しています。訪問者が S3 の URL 経由でオブジェクトに到達できないようにする必要があります。これを実現する 2 つのアクションはどれですか。",
      ["バケットで S3 ブロックパブリックアクセスを有効にし、公開読み取りのバケットポリシーや ACL を削除する",
       "CloudFront のオリジンにオリジンアクセスコントロール (OAC) をアタッチし、その CloudFront ディストリビューションにのみ s3:GetObject を許可するバケットポリシーを追加する",
       "バケットを S3 静的ウェブサイトエンドポイントとして構成し、ネットワーク ACL で制限する",
       "バケットを VPC のプライベートサブネットに移動する",
       "バケットで S3 リクエスタ支払いを有効にする"],
      "オリジンアクセスコントロールを使うと、CloudFront は S3 へのリクエストを SigV4 で署名します。バケットポリシーでは CloudFront のサービスプリンシパルに対し、ディストリビューションを指定した aws:SourceArn 条件付きで s3:GetObject を許可するため、他の呼び出し元は成功しません。ブロックパブリックアクセスは、残存する公開 ACL やポリシーによってバケットが再び開かれないことを保証します。選択肢 c は本末転倒で、S3 ウェブサイトエンドポイントは設計上公開であり、ネットワーク ACL は S3 には適用されません。選択肢 d は不可能です。S3 はリージョンサービスであって VPC リソースではなく、サブネットを持ちません。選択肢 e が変えるのは請求先であって、アクセス可否ではありません。"),
  zh=("某静态网站通过 Amazon CloudFront 提供，源站为 Amazon S3 存储桶。访问者不得通过 S3 URL 直接访问这些对象。哪两项操作组合可以实现这一点？",
      ["对该存储桶启用 S3 阻止公有访问，并删除任何公开读取的存储桶策略或 ACL",
       "为 CloudFront 源站附加源访问控制（OAC），并添加仅允许该 CloudFront 分配执行 s3:GetObject 的存储桶策略",
       "将该存储桶配置为 S3 静态网站终端节点，并用网络 ACL 加以限制",
       "把该存储桶移入 VPC 的私有子网",
       "对该存储桶启用 S3 请求者付费"],
      "源访问控制让 CloudFront 使用 SigV4 对发往 S3 的请求签名；随后存储桶策略仅向 CloudFront 服务主体授予 s3:GetObject，并通过 aws:SourceArn 条件指定该分配，其他调用者都无法成功。阻止公有访问可确保不会有遗留的公开 ACL 或策略在背后重新打开存储桶。选项 c 自相矛盾：S3 网站终端节点在设计上就是公开的，而网络 ACL 根本不适用于 S3。选项 d 不可能实现：S3 是区域级服务，不是 VPC 资源，没有子网。选项 e 改变的是谁付费，而不是谁可以访问。"))

Q("aws-saa-secure-10", "secure_architectures",
  "Domain 1, Task Statement 1.3 (Determine appropriate data security controls)",
  False, False, SC, ["c"],
  "docs.aws.amazon.com/elasticloadbalancing/latest/application/create-https-listener.html and docs.aws.amazon.com/acm/latest/userguide/acm-services.html",
  en=("A company terminates TLS on an Application Load Balancer using a public certificate issued by AWS Certificate Manager (ACM). A new control requires that traffic between the load balancer and the EC2 targets also be encrypted. What is the correct approach?",
      ["Export the private key of the load balancer's existing ACM public certificate and install it on the EC2 instances",
       "Place a Network Load Balancer in front of the Application Load Balancer, which encrypts backend traffic automatically",
       "Set the target group protocol to HTTPS and install a certificate on the instances, for example one issued by AWS Private Certificate Authority",
       "Enable server-side encryption on the load balancer's access log bucket"],
      "Backend encryption is configured by setting the target group's protocol to HTTPS. The ALB then encrypts the connection to the target but does not validate the target's certificate chain, which is why a certificate from a private CA (or even a self-signed one) is acceptable, and AWS Private CA is the tidy way to issue one. Option a fails on two counts. First, an ordinary ACM public certificate is not exportable: since 17 June 2025 ACM does offer separately-charged exportable public certificates, but that has to be chosen when the certificate is requested and does not retroactively make an existing certificate exportable. Second, reusing the internet-facing certificate on the backend is not how backend encryption is configured in any case. Putting an NLB in front encrypts nothing by itself, and access-log encryption concerns stored logs rather than traffic in transit."),
  de=("Ein Unternehmen terminiert TLS an einem Application Load Balancer mit einem öffentlichen Zertifikat aus AWS Certificate Manager (ACM). Eine neue Vorgabe verlangt, dass auch der Verkehr zwischen Load Balancer und den EC2-Zielen verschlüsselt ist. Was ist der richtige Weg?",
      ["Den privaten Schlüssel des vorhandenen öffentlichen ACM-Zertifikats des Load Balancers exportieren und auf den EC2-Instanzen installieren",
       "Einen Network Load Balancer vor den Application Load Balancer setzen, der den Backend-Verkehr automatisch verschlüsselt",
       "Das Protokoll der Zielgruppe auf HTTPS setzen und auf den Instanzen ein Zertifikat installieren, etwa eines aus AWS Private Certificate Authority",
       "Serverseitige Verschlüsselung für den Bucket der Zugriffsprotokolle des Load Balancers aktivieren"],
      "Die Backend-Verschlüsselung wird konfiguriert, indem das Protokoll der Zielgruppe auf HTTPS gesetzt wird. Der ALB verschlüsselt dann zum Ziel hin, prüft dessen Zertifikatskette aber nicht - deshalb genügt ein Zertifikat aus einer privaten CA (oder sogar ein selbstsigniertes), und AWS Private CA ist der saubere Weg, es auszustellen. Antwort a scheitert doppelt. Erstens ist ein gewöhnliches öffentliches ACM-Zertifikat nicht exportierbar: Seit dem 17. Juni 2025 bietet ACM zwar gesondert berechnete exportierbare öffentliche Zertifikate an, das muss aber bei der Anforderung des Zertifikats gewählt werden und macht ein bestehendes Zertifikat nicht nachträglich exportierbar. Zweitens ist die Wiederverwendung des nach außen gerichteten Zertifikats im Backend ohnehin nicht der Weg, Backend-Verschlüsselung zu konfigurieren. Ein vorgeschalteter NLB verschlüsselt von sich aus gar nichts, und die Verschlüsselung von Zugriffsprotokollen betrifft gespeicherte Logs, nicht den Verkehr."),
  ja=("ある企業は、AWS Certificate Manager (ACM) が発行したパブリック証明書を使って Application Load Balancer で TLS を終端しています。新しい統制要件により、ロードバランサーと EC2 ターゲット間の通信も暗号化する必要が生じました。正しい方法はどれですか。",
      ["ロードバランサーが使用している既存の ACM パブリック証明書の秘密鍵をエクスポートし、EC2 インスタンスにインストールする",
       "Application Load Balancer の前段に Network Load Balancer を置く。これによりバックエンド通信が自動的に暗号化される",
       "ターゲットグループのプロトコルを HTTPS に設定し、インスタンスに証明書(例えば AWS Private Certificate Authority が発行したもの)をインストールする",
       "ロードバランサーのアクセスログ用バケットでサーバー側暗号化を有効にする"],
      "バックエンド暗号化はターゲットグループのプロトコルを HTTPS に設定して構成します。ALB はターゲットへの接続を暗号化しますが、ターゲットの証明書チェーンは検証しません。だからこそプライベート CA 発行の証明書(自己署名でも可)で十分であり、AWS Private CA はその発行手段として妥当です。選択肢 a は二重に誤りです。第一に、通常の ACM パブリック証明書はエクスポートできません。2025 年 6 月 17 日以降、ACM は別料金のエクスポート可能なパブリック証明書を提供していますが、それは証明書の申請時に選択する必要があり、既存の証明書を後からエクスポート可能にするものではありません。第二に、インターネット向けの証明書をバックエンドで使い回すことは、そもそもバックエンド暗号化の構成方法ではありません。前段に NLB を置いてもそれ自体は何も暗号化せず、アクセスログの暗号化は保存済みログの話で通信中のデータとは無関係です。"),
  zh=("某公司使用 AWS Certificate Manager（ACM）签发的公有证书在 Application Load Balancer 上终止 TLS。新的合规控制要求负载均衡器与 EC2 目标之间的流量也必须加密。正确的做法是什么？",
      ["导出负载均衡器现有 ACM 公有证书的私钥并安装到 EC2 实例上",
       "在 Application Load Balancer 前面再放一个 Network Load Balancer，它会自动加密后端流量",
       "将目标组协议设置为 HTTPS，并在实例上安装证书，例如由 AWS Private Certificate Authority 签发的证书",
       "为负载均衡器访问日志所在的存储桶启用服务器端加密"],
      "后端加密的配置方式是把目标组协议设为 HTTPS；此时 ALB 会加密到目标的连接，但不会校验目标的证书链，正因如此私有 CA 签发的证书（甚至自签名证书）也可接受，而 AWS Private CA 是签发它的规范方式。选项 a 有两处错误。其一，普通的 ACM 公有证书不可导出：自 2025 年 6 月 17 日起 ACM 确实提供单独计费的可导出公有证书，但这必须在申请证书时选择，并不会让已有证书事后变为可导出。其二，把面向互联网的证书拿到后端复用，本来也不是配置后端加密的方式。在前面加一个 NLB 本身不会加密任何东西，而访问日志加密关注的是已存储的日志，不是传输中的流量。"))

Q("aws-saa-secure-11", "secure_architectures",
  "Domain 1, Task Statement 1.1 (Design secure access to AWS resources)",
  True, True, MC, ["a", "c"],
  "docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html",
  en=("A new AWS account has just been created. Which TWO actions are baseline security recommendations for the account root user?",
      ["Enable multi-factor authentication (MFA) on the root user",
       "Create long-lived root access keys so that automation can use them",
       "Delete any root user access keys and use IAM roles or AWS IAM Identity Center principals for day-to-day work",
       "Attach the AdministratorAccess managed policy to the root user so its permissions are explicit",
       "Share the root credentials with at least three administrators so that access is never lost"],
      "The root user should be protected by MFA, should have no access keys at all, and should be used only for the small set of tasks that genuinely require it. Everyday work belongs to IAM roles or IAM Identity Center principals under least privilege. Options b and e both create long-lived, widely-held credentials for the one identity that cannot be restricted. Option d is meaningless: the root user's power does not come from an attached policy and cannot be defined or limited by one."),
  de=("Ein neues AWS-Konto wurde gerade angelegt. Welche ZWEI Maßnahmen sind grundlegende Sicherheitsempfehlungen für den Root-Benutzer des Kontos?",
      ["Multi-Faktor-Authentifizierung (MFA) für den Root-Benutzer aktivieren",
       "Langlebige Root-Zugriffsschlüssel erstellen, damit Automatisierung sie nutzen kann",
       "Alle Zugriffsschlüssel des Root-Benutzers löschen und für die tägliche Arbeit IAM-Rollen oder Prinzipale aus AWS IAM Identity Center verwenden",
       "Dem Root-Benutzer die verwaltete Richtlinie AdministratorAccess zuweisen, damit seine Berechtigungen explizit sind",
       "Die Root-Anmeldeinformationen mit mindestens drei Administratoren teilen, damit der Zugang nie verloren geht"],
      "Der Root-Benutzer sollte durch MFA geschützt sein, überhaupt keine Zugriffsschlüssel besitzen und nur für die wenigen Aufgaben verwendet werden, die ihn wirklich erfordern. Die tägliche Arbeit gehört zu IAM-Rollen oder Identity-Center-Prinzipalen nach dem Least-Privilege-Prinzip. Die Antworten b und e erzeugen beide langlebige, breit verteilte Anmeldeinformationen für genau die eine Identität, die sich nicht einschränken lässt. Antwort d ist sinnlos: Die Macht des Root-Benutzers stammt nicht aus einer angehängten Richtlinie und lässt sich durch eine solche weder definieren noch begrenzen."),
  ja=("新しい AWS アカウントを作成した直後です。アカウントのルートユーザーに対する基本的なセキュリティ推奨事項はどの 2 つですか。",
      ["ルートユーザーで多要素認証 (MFA) を有効にする",
       "自動化から利用できるよう、長期間有効なルートアクセスキーを作成する",
       "ルートユーザーのアクセスキーをすべて削除し、日常業務には IAM ロールまたは AWS IAM Identity Center のプリンシパルを使う",
       "権限を明示するために、ルートユーザーに AdministratorAccess 管理ポリシーをアタッチする",
       "アクセスを失わないよう、ルートの認証情報を少なくとも 3 名の管理者と共有する"],
      "ルートユーザーは MFA で保護し、アクセスキーを一切持たせず、本当にルートでしかできない少数の作業にのみ使うべきです。日常業務は最小権限に基づく IAM ロールや IAM Identity Center のプリンシパルの仕事です。選択肢 b と e はいずれも、制限できない唯一の ID に対して長期かつ広く共有された認証情報を作ってしまいます。選択肢 d は無意味です。ルートユーザーの権限はアタッチされたポリシーに由来するものではなく、ポリシーで定義することも制限することもできません。"),
  zh=("刚刚创建了一个新的 AWS 账户。针对账户根用户的基线安全建议是哪两项？",
      ["为根用户启用多重身份验证（MFA）",
       "创建长期有效的根用户访问密钥，供自动化流程使用",
       "删除根用户的所有访问密钥，日常工作改用 IAM 角色或 AWS IAM Identity Center 主体",
       "为根用户附加 AdministratorAccess 托管策略，使其权限更明确",
       "把根用户凭证分享给至少三名管理员，以免失去访问权限"],
      "根用户应当启用 MFA、完全不持有访问密钥，并且仅用于确实必须由其执行的少数任务。日常工作应交给遵循最小权限的 IAM 角色或 IAM Identity Center 主体。选项 b 和 e 都是为唯一一个无法被限制的身份创建长期且被广泛持有的凭证。选项 d 毫无意义：根用户的权限并非来自所附加的策略，也无法通过策略来定义或限制。"))

# =====================================================================
# Domain 2 - Design Resilient Architectures (26% of scored content) - 9 Q
# =====================================================================

Q("aws-saa-resilient-01", "resilient_architectures",
  "Domain 2, Task Statement 2.1 (Design scalable and loosely coupled architectures)",
  True, False, SC, ["c"],
  "docs.aws.amazon.com/autoscaling/ec2/userguide/as-using-sqs-queue.html",
  en=("A web tier posts order records directly to a worker fleet over HTTP. During traffic spikes the workers cannot keep up and orders are lost. Which change addresses this with the least operational overhead?",
      ["Increase the web tier instance size so that it can retry the failed calls for longer",
       "Move the workers behind an Application Load Balancer with sticky sessions enabled",
       "Put an Amazon SQS queue between the tiers and scale the worker Auto Scaling group on the queue's backlog per instance",
       "Have the web tier write the orders to a shared Amazon EBS volume that all workers mount"],
      "A queue decouples producer from consumer: the spike lands in durable storage instead of being dropped, and scaling the worker Auto Scaling group on backlog per instance ties capacity to the work actually waiting rather than to CPU. Option a only postpones the failure and still loses orders when retries are exhausted. Sticky sessions distribute load, they do not buffer it. Option d is not possible as described: a standard EBS volume attaches to one instance at a time and lives in a single Availability Zone."),
  de=("Eine Web-Schicht sendet Bestelldatensätze direkt per HTTP an eine Worker-Flotte. Bei Lastspitzen kommen die Worker nicht mit und Bestellungen gehen verloren. Welche Änderung löst das mit dem geringsten Betriebsaufwand?",
      ["Die Instanzgröße der Web-Schicht erhöhen, damit sie fehlgeschlagene Aufrufe länger wiederholen kann",
       "Die Worker hinter einen Application Load Balancer mit aktivierten Sticky Sessions stellen",
       "Eine Amazon-SQS-Warteschlange zwischen die Schichten setzen und die Auto-Scaling-Gruppe der Worker anhand des Rückstands pro Instanz skalieren",
       "Die Web-Schicht die Bestellungen auf ein gemeinsames Amazon-EBS-Volume schreiben lassen, das alle Worker einhängen"],
      "Eine Warteschlange entkoppelt Erzeuger und Verbraucher: Die Spitze landet in dauerhaftem Speicher, statt verworfen zu werden, und die Skalierung der Worker-Auto-Scaling-Gruppe anhand des Rückstands pro Instanz koppelt die Kapazität an die tatsächlich wartende Arbeit statt an die CPU. Antwort a verschiebt den Fehler nur und verliert Bestellungen, sobald die Wiederholungen aufgebraucht sind. Sticky Sessions verteilen Last, puffern sie aber nicht. Antwort d ist so nicht möglich: Ein gewöhnliches EBS-Volume ist jeweils an eine Instanz angehängt und liegt in einer einzigen Availability Zone."),
  ja=("ウェブ層が注文レコードを HTTP でワーカー群に直接送信しています。トラフィックの急増時にワーカーが処理しきれず、注文が失われています。運用負荷が最も小さい対処はどれですか。",
      ["ウェブ層のインスタンスサイズを大きくし、失敗した呼び出しをより長くリトライできるようにする",
       "ワーカーをスティッキーセッション有効の Application Load Balancer の背後に配置する",
       "層の間に Amazon SQS キューを置き、キューのインスタンスあたりバックログに基づいてワーカーの Auto Scaling グループをスケールさせる",
       "ウェブ層が注文を共有の Amazon EBS ボリュームに書き込み、全ワーカーがそれをマウントする"],
      "キューは生成側と消費側を疎結合にします。急増分は破棄されずに永続ストレージへ入り、インスタンスあたりバックログでワーカーの Auto Scaling グループをスケールさせれば、CPU ではなく実際に待機している仕事量に容量が連動します。選択肢 a は失敗を先送りするだけで、リトライを使い切れば結局注文は失われます。スティッキーセッションは負荷を分散するだけでバッファリングはしません。選択肢 d は記述どおりには実現できません。通常の EBS ボリュームは一度に 1 つのインスタンスにしかアタッチできず、単一のアベイラビリティーゾーンに存在します。"),
  zh=("Web 层通过 HTTP 将订单记录直接发送给工作节点集群。流量高峰时工作节点跟不上，导致订单丢失。哪项变更能以最小的运维开销解决该问题？",
      ["增大 Web 层实例规格，使其能够对失败调用重试更长时间",
       "把工作节点放到启用了粘性会话的 Application Load Balancer 之后",
       "在两层之间加入 Amazon SQS 队列，并根据队列的每实例积压量对工作节点 Auto Scaling 组进行伸缩",
       "让 Web 层把订单写入一个所有工作节点都挂载的共享 Amazon EBS 卷"],
      "队列可将生产者与消费者解耦：高峰流量进入持久化存储而不是被丢弃；按每实例积压量伸缩工作节点 Auto Scaling 组，使容量与真正待处理的工作量而非 CPU 挂钩。选项 a 只是推迟失败，重试耗尽后订单照样丢失。粘性会话只分配负载，不做缓冲。选项 d 按描述根本无法实现：普通 EBS 卷同一时刻只能挂载到一台实例，且位于单个可用区内。"))

Q("aws-saa-resilient-02", "resilient_architectures",
  "Domain 2, Task Statement 2.1 (Design scalable and loosely coupled architectures)",
  True, False, SC, ["a"],
  "docs.aws.amazon.com/sns/latest/dg/sns-common-scenarios.html",
  en=("One business event must reach three independent processing pipelines. Each pipeline must be able to fail, retry and fall behind without affecting the other two. Which design is appropriate?",
      ["Publish the event to an Amazon SNS topic to which three Amazon SQS queues are subscribed, one per pipeline",
       "Write the event to a single Amazon SQS queue that all three pipelines poll",
       "Have the producer invoke the three pipelines synchronously, one after another",
       "Write the event to Amazon S3 and have each pipeline list the bucket every minute"],
      "This is the fan-out pattern: SNS delivers a copy of each message to every subscribed queue, so each consumer gets its own buffer, its own visibility timeout, its own retry behaviour and its own dead-letter queue. A single shared queue is the opposite: each message is delivered to one consumer only, so the three pipelines would compete for messages. Synchronous invocation re-couples the producer to the slowest consumer. Polling S3 adds latency, cost and a listing-consistency problem for no benefit."),
  de=("Ein Geschäftsereignis muss drei unabhängige Verarbeitungsstrecken erreichen. Jede Strecke muss ausfallen, wiederholen und zurückfallen können, ohne die beiden anderen zu beeinträchtigen. Welcher Entwurf ist passend?",
      ["Das Ereignis in einem Amazon-SNS-Thema veröffentlichen, das drei Amazon-SQS-Warteschlangen abonniert haben, eine je Strecke",
       "Das Ereignis in eine einzige Amazon-SQS-Warteschlange schreiben, die alle drei Strecken abfragen",
       "Den Erzeuger die drei Strecken nacheinander synchron aufrufen lassen",
       "Das Ereignis nach Amazon S3 schreiben und jede Strecke den Bucket jede Minute auflisten lassen"],
      "Das ist das Fan-out-Muster: SNS stellt jeder abonnierten Warteschlange eine Kopie jeder Nachricht zu, sodass jeder Verbraucher seinen eigenen Puffer, sein eigenes Sichtbarkeits-Timeout, sein eigenes Wiederholungsverhalten und seine eigene Dead-Letter-Queue hat. Eine einzige gemeinsame Warteschlange ist das Gegenteil: Jede Nachricht geht an genau einen Verbraucher, die drei Strecken würden also um Nachrichten konkurrieren. Der synchrone Aufruf koppelt den Erzeuger wieder an den langsamsten Verbraucher. S3 abzufragen kostet Latenz und Geld und bringt nichts."),
  ja=("1 つのビジネスイベントを 3 つの独立した処理パイプラインに届ける必要があります。各パイプラインは、他の 2 つに影響を与えずに障害・リトライ・遅延できなければなりません。適切な設計はどれですか。",
      ["イベントを Amazon SNS トピックに発行し、そのトピックにパイプラインごとに 1 つずつ、計 3 つの Amazon SQS キューをサブスクライブさせる",
       "イベントを 1 つの Amazon SQS キューに書き込み、3 つのパイプラインすべてがそれをポーリングする",
       "プロデューサーが 3 つのパイプラインを順に同期的に呼び出す",
       "イベントを Amazon S3 に書き込み、各パイプラインが毎分バケットを一覧する"],
      "これはファンアウトパターンです。SNS はサブスクライブされた各キューにメッセージのコピーを配信するため、各コンシューマーが独自のバッファ、可視性タイムアウト、リトライ動作、デッドレターキューを持てます。単一の共有キューはその逆で、各メッセージは 1 つのコンシューマーにしか届かず、3 つのパイプラインがメッセージを奪い合うことになります。同期呼び出しはプロデューサーを最も遅いコンシューマーに再び結合します。S3 のポーリングは遅延とコストを増やすだけです。"),
  zh=("一个业务事件必须送达三条相互独立的处理流水线。每条流水线都必须能够独立失败、重试和积压，而不影响另外两条。哪种设计是合适的？",
      ["将事件发布到 Amazon SNS 主题，并让三个 Amazon SQS 队列各自订阅该主题，每条流水线一个队列",
       "将事件写入一个 Amazon SQS 队列，三条流水线都轮询该队列",
       "由生产者依次同步调用这三条流水线",
       "将事件写入 Amazon S3，每条流水线每分钟列举一次存储桶"],
      "这是扇出（fan-out）模式：SNS 会向每个订阅队列投递一份消息副本，因此每个消费者拥有自己的缓冲、可见性超时、重试行为和死信队列。单个共享队列恰恰相反：每条消息只投递给一个消费者，三条流水线会互相抢夺消息。同步调用又把生产者绑定到最慢的消费者上。轮询 S3 只会增加延迟和成本，毫无收益。"))

Q("aws-saa-resilient-03", "resilient_architectures",
  "Domain 2, Task Statement 2.2 (Design highly available and/or fault-tolerant architectures)",
  False, True, SC, ["d"],
  "docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZSingleStandby.html",
  en=("An Amazon RDS for PostgreSQL database runs as a Multi-AZ DB instance deployment. Reporting queries are saturating the primary, and a team member proposes pointing the reports at the standby. What should the solutions architect say?",
      ["It works, because the standby is a synchronous copy and is therefore available for reads",
       "It works, but only if the reports connect through the cluster reader endpoint",
       "It works once the standby's public accessibility setting is enabled",
       "It does not work: the standby in a Multi-AZ DB instance deployment cannot serve read traffic, so add a read replica or move to a Multi-AZ DB cluster deployment"],
      "AWS states it plainly: the Multi-AZ high-availability option is not a scaling solution for read-only scenarios, and you cannot use a standby replica to serve read traffic. The standby exists to be promoted on failover. To offload reads you either add read replicas (asynchronous, with a small lag) or use a Multi-AZ DB cluster deployment, which has two readable standby instances and a reader endpoint. A Multi-AZ DB instance deployment has no reader endpoint, and public accessibility is irrelevant to the question."),
  de=("Eine Amazon-RDS-für-PostgreSQL-Datenbank läuft als Multi-AZ-DB-Instance-Bereitstellung. Auswertungsabfragen lasten die primäre Instanz aus, und ein Teammitglied schlägt vor, die Auswertungen auf den Standby zu richten. Was sollte die Lösungsarchitektin sagen?",
      ["Es funktioniert, weil der Standby eine synchrone Kopie und damit für Lesezugriffe verfügbar ist",
       "Es funktioniert, aber nur wenn die Auswertungen über den Cluster-Reader-Endpunkt verbinden",
       "Es funktioniert, sobald die Einstellung für öffentliche Erreichbarkeit des Standby aktiviert ist",
       "Es funktioniert nicht: Der Standby einer Multi-AZ-DB-Instance-Bereitstellung kann keinen Leseverkehr bedienen; also ein Read Replica ergänzen oder auf eine Multi-AZ-DB-Cluster-Bereitstellung wechseln"],
      "AWS sagt es unmissverständlich: Die Multi-AZ-Hochverfügbarkeitsoption ist keine Skalierungslösung für Nur-Lese-Szenarien, und ein Standby-Replikat kann keinen Leseverkehr bedienen. Der Standby existiert, um bei einem Failover befördert zu werden. Zum Auslagern von Lesezugriffen ergänzt man entweder Read Replicas (asynchron, mit geringem Nachlauf) oder wechselt auf eine Multi-AZ-DB-Cluster-Bereitstellung mit zwei lesbaren Standby-Instanzen und einem Reader-Endpunkt. Eine Multi-AZ-DB-Instance-Bereitstellung hat keinen Reader-Endpunkt, und die öffentliche Erreichbarkeit ist hier bedeutungslos."),
  ja=("Amazon RDS for PostgreSQL のデータベースが Multi-AZ DB インスタンス配置で稼働しています。レポート用クエリがプライマリを飽和させており、チームメンバーがレポートをスタンバイに向けることを提案しました。ソリューションアーキテクトは何と答えるべきですか。",
      ["スタンバイは同期コピーなので読み取りに利用でき、うまくいく",
       "レポートがクラスターリーダーエンドポイント経由で接続する場合に限りうまくいく",
       "スタンバイのパブリックアクセス設定を有効にすればうまくいく",
       "うまくいかない。Multi-AZ DB インスタンス配置のスタンバイは読み取りトラフィックを処理できないため、リードレプリカを追加するか Multi-AZ DB クラスター配置へ移行する"],
      "AWS は明確に述べています。Multi-AZ の高可用性オプションは読み取り専用シナリオのスケーリング手段ではなく、スタンバイレプリカを読み取りトラフィックに使うことはできません。スタンバイはフェイルオーバー時に昇格するために存在します。読み取りをオフロードするには、リードレプリカ(非同期でわずかな遅延あり)を追加するか、読み取り可能なスタンバイ 2 台とリーダーエンドポイントを持つ Multi-AZ DB クラスター配置を使います。Multi-AZ DB インスタンス配置にリーダーエンドポイントは存在せず、パブリックアクセス設定はこの問いとは無関係です。"),
  zh=("某 Amazon RDS for PostgreSQL 数据库以 Multi-AZ 数据库实例部署方式运行。报表查询正在压满主实例，有团队成员建议把报表指向备用实例。解决方案架构师应如何回应？",
      ["可行，因为备用实例是同步副本，因此可用于读取",
       "可行，但报表必须通过集群读取器终端节点连接",
       "启用备用实例的公开可访问性设置后即可行",
       "不可行：Multi-AZ 数据库实例部署中的备用实例无法处理读取流量，应增加只读副本或改用 Multi-AZ 数据库集群部署"],
      "AWS 的说明很直接：Multi-AZ 高可用选项不是只读场景的扩展方案，备用副本不能用于处理读取流量。备用实例的存在是为了在故障转移时被提升为主实例。要卸载读取压力，可以增加只读副本（异步，存在少量延迟），或改用具有两个可读备用实例和读取器终端节点的 Multi-AZ 数据库集群部署。Multi-AZ 数据库实例部署没有读取器终端节点，而公开可访问性设置与本题无关。"))

Q("aws-saa-resilient-04", "resilient_architectures",
  "Domain 2, Task Statement 2.2 (Design highly available and/or fault-tolerant architectures)",
  False, True, SC, ["b"],
  "docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-basics.html",
  en=("A VPC has private subnets in three Availability Zones. All three route 0.0.0.0/0 to a single NAT gateway that lives in Availability Zone A. What is the resilience consequence, and what is the fix?",
      ["There is none: a NAT gateway is a Regional construct and is unaffected by the loss of one Availability Zone",
       "If Availability Zone A fails, workloads in the other two zones lose outbound internet access; create a NAT gateway in each zone and point each subnet's route table at the NAT gateway in its own zone",
       "There is none: a NAT gateway automatically fails over to the internet gateway",
       "Connectivity is fine but cross-zone charges are higher; the fix is to consolidate all workloads into Availability Zone A"],
      "AWS states that each NAT gateway is created in a specific Availability Zone and is implemented with redundancy only within that zone, and recommends creating one per zone with same-zone routing precisely because a shared NAT gateway makes one zone's failure everyone's failure. The same change also removes the cross-AZ data transfer charge on the outbound path. There is no failover to the internet gateway: private subnets have no route to it, which is what makes them private."),
  de=("Eine VPC hat private Subnetze in drei Availability Zones. Alle drei routen 0.0.0.0/0 auf ein einziges NAT-Gateway in Availability Zone A. Welche Folge hat das für die Ausfallsicherheit, und wie lautet die Korrektur?",
      ["Keine: Ein NAT-Gateway ist ein regionales Konstrukt und vom Ausfall einer Availability Zone nicht betroffen",
       "Fällt Availability Zone A aus, verlieren die Workloads in den beiden anderen Zonen den ausgehenden Internetzugang; je Zone ein NAT-Gateway anlegen und die Routing-Tabelle jedes Subnetzes auf das NAT-Gateway der eigenen Zone zeigen lassen",
       "Keine: Ein NAT-Gateway fällt automatisch auf das Internet-Gateway zurück",
       "Die Konnektivität ist in Ordnung, nur die zonenübergreifenden Gebühren sind höher; die Korrektur besteht darin, alle Workloads in Availability Zone A zu bündeln"],
      "Laut AWS wird jedes NAT-Gateway in einer bestimmten Availability Zone angelegt und ist nur innerhalb dieser Zone redundant ausgelegt; AWS empfiehlt genau deshalb je Zone ein Gateway mit zoneninternem Routing, weil ein gemeinsames NAT-Gateway den Ausfall einer Zone zum Ausfall aller macht. Dieselbe Änderung beseitigt zusätzlich die zonenübergreifende Datenübertragungsgebühr auf dem ausgehenden Pfad. Ein Rückfall auf das Internet-Gateway gibt es nicht: Private Subnetze haben keine Route dorthin - genau das macht sie privat."),
  ja=("ある VPC は 3 つのアベイラビリティーゾーンにプライベートサブネットを持ち、いずれも 0.0.0.0/0 をアベイラビリティーゾーン A にある 1 つの NAT ゲートウェイにルーティングしています。可用性上の影響と、その是正策はどれですか。",
      ["影響はない。NAT ゲートウェイはリージョンレベルの構成要素であり、1 つのアベイラビリティーゾーンの障害の影響を受けない",
       "アベイラビリティーゾーン A が障害を起こすと、他の 2 ゾーンのワークロードがアウトバウンドのインターネット接続を失う。各ゾーンに NAT ゲートウェイを作成し、各サブネットのルートテーブルを自ゾーンの NAT ゲートウェイに向ける",
       "影響はない。NAT ゲートウェイはインターネットゲートウェイへ自動的にフェイルオーバーする",
       "接続性に問題はないがゾーン間料金が高くなる。是正策はすべてのワークロードをアベイラビリティーゾーン A に集約すること"],
      "AWS は、各 NAT ゲートウェイは特定のアベイラビリティーゾーンに作成され、そのゾーン内でのみ冗長化されていると明記しています。共有 NAT ゲートウェイでは 1 ゾーンの障害が全体の障害になるため、ゾーンごとに NAT ゲートウェイを作り同一ゾーン内でルーティングすることが推奨されています。この変更はアウトバウンド経路のゾーン間データ転送料金も解消します。インターネットゲートウェイへのフェイルオーバーは存在しません。プライベートサブネットにはそこへのルートがなく、それこそがプライベートである理由です。"),
  zh=("某 VPC 在三个可用区中都有私有子网，三者的 0.0.0.0/0 都指向位于可用区 A 的同一个 NAT 网关。这带来什么可用性后果，应如何修复？",
      ["没有后果：NAT 网关是区域级构件，不受单个可用区故障影响",
       "若可用区 A 发生故障，另外两个可用区的工作负载将失去出站互联网访问；应在每个可用区各创建一个 NAT 网关，并让各子网的路由表指向本可用区的 NAT 网关",
       "没有后果：NAT 网关会自动故障转移到互联网网关",
       "连通性没问题，只是跨可用区费用更高；修复办法是把所有工作负载集中到可用区 A"],
      "AWS 明确指出，每个 NAT 网关都创建在特定可用区中，并且仅在该可用区内实现冗余；正因为共享 NAT 网关会使一个可用区的故障变成所有可用区的故障，AWS 建议每个可用区各建一个并在同可用区内路由。这一改动还顺带消除了出站路径上的跨可用区数据传输费用。不存在向互联网网关的故障转移：私有子网没有通往互联网网关的路由，这正是它之所以“私有”的原因。"))

Q("aws-saa-resilient-05", "resilient_architectures",
  "Domain 2, Task Statement 2.2 (Design highly available and/or fault-tolerant architectures)",
  False, False, SC, ["a"],
  "docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy-failover.html",
  en=("A company wants a low-cost disaster-recovery target for a public website: while the primary Region's endpoint is healthy it should serve all traffic, and if it becomes unhealthy visitors should be served a read-only static version instead. Which Amazon Route 53 configuration does this?",
      ["A failover routing policy, with a health check on the primary record and the static site as the secondary record",
       "A weighted routing policy that sends 99 percent of traffic to the primary and 1 percent to the static site",
       "A latency-based routing policy across the primary endpoint and the static site",
       "A multivalue answer routing policy returning both endpoints"],
      "Failover routing is the active-passive policy: Route 53 returns the secondary record only when the associated health check on the primary reports unhealthy, which is exactly the described behaviour. Weighted, latency-based and multivalue answer policies all send some share of normal traffic to both endpoints, so users would intermittently land on the read-only site while the primary is perfectly healthy."),
  de=("Ein Unternehmen möchte ein kostengünstiges Notfallziel für eine öffentliche Website: Solange der Endpunkt in der primären Region gesund ist, soll er den gesamten Verkehr bedienen; wird er ungesund, sollen Besucher stattdessen eine schreibgeschützte statische Fassung erhalten. Welche Amazon-Route-53-Konfiguration leistet das?",
      ["Eine Failover-Routing-Richtlinie mit einer Integritätsprüfung auf dem primären Eintrag und der statischen Website als sekundärem Eintrag",
       "Eine gewichtete Routing-Richtlinie, die 99 Prozent des Verkehrs an den primären Endpunkt und 1 Prozent an die statische Website sendet",
       "Eine latenzbasierte Routing-Richtlinie über den primären Endpunkt und die statische Website",
       "Eine Multivalue-Answer-Routing-Richtlinie, die beide Endpunkte zurückgibt"],
      "Failover-Routing ist die Aktiv-Passiv-Richtlinie: Route 53 liefert den sekundären Eintrag nur dann aus, wenn die zugehörige Integritätsprüfung des primären Eintrags als ungesund meldet - genau das beschriebene Verhalten. Gewichtete, latenzbasierte und Multivalue-Answer-Richtlinien senden jeweils einen Anteil des normalen Verkehrs an beide Endpunkte; Nutzer würden also zeitweise auf der schreibgeschützten Seite landen, obwohl der primäre Endpunkt völlig gesund ist."),
  ja=("ある企業は、公開ウェブサイト向けに低コストな災害復旧先を用意したいと考えています。プライマリリージョンのエンドポイントが正常な間はすべてのトラフィックを処理し、異常になったら訪問者には読み取り専用の静的版を提供する、という動作です。これを実現する Amazon Route 53 の設定はどれですか。",
      ["フェイルオーバールーティングポリシー。プライマリレコードにヘルスチェックを設定し、静的サイトをセカンダリレコードにする",
       "加重ルーティングポリシーで、トラフィックの 99 パーセントをプライマリに、1 パーセントを静的サイトに送る",
       "プライマリエンドポイントと静的サイトにまたがるレイテンシーベースルーティングポリシー",
       "両方のエンドポイントを返す複数値回答ルーティングポリシー"],
      "フェイルオーバールーティングはアクティブ/パッシブ用のポリシーです。Route 53 は、プライマリに紐づくヘルスチェックが異常を報告したときにのみセカンダリレコードを返します。これはまさに求められている挙動です。加重・レイテンシーベース・複数値回答の各ポリシーは、いずれも通常時のトラフィックの一部を両方のエンドポイントに振り分けるため、プライマリが完全に正常でも一部の利用者が読み取り専用サイトに到達してしまいます。"),
  zh=("某公司希望为一个公开网站建立低成本的灾备目标：主区域终端节点健康时承载全部流量，一旦不健康则改为向访问者提供只读的静态版本。哪种 Amazon Route 53 配置能做到这一点？",
      ["故障转移路由策略：对主记录配置运行状况检查，并将静态站点作为辅助记录",
       "加权路由策略：把 99% 的流量发往主端点，1% 发往静态站点",
       "在主端点与静态站点之间使用基于延迟的路由策略",
       "返回两个端点的多值应答路由策略"],
      "故障转移路由正是主备（active-passive）策略：只有当主记录关联的运行状况检查报告不健康时，Route 53 才返回辅助记录，这与题目描述完全一致。加权、基于延迟和多值应答策略都会在正常情况下把一部分流量分配给两个端点，用户会在主端点完全健康时也偶尔落到只读站点上。"))

Q("aws-saa-resilient-06", "resilient_architectures",
  "Domain 2, Task Statement 2.1 (Design scalable and loosely coupled architectures)",
  False, False, SC, ["c"],
  "docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues.html",
  en=("A payment workflow requires that messages for any one customer are processed in the exact order they were sent, that a duplicate submission inside the deduplication interval is not processed twice, and that different customers can still be processed in parallel. Which Amazon SQS configuration meets this?",
      ["A standard queue with a visibility timeout longer than the processing time",
       "A standard queue with long polling enabled",
       "A FIFO queue using the customer identifier as the message group ID, with content-based deduplication enabled",
       "A FIFO queue with every message in a single message group and deduplication disabled"],
      "FIFO queues guarantee ordering within a message group and exactly-once processing within the five-minute deduplication interval. Using the customer identifier as the message group ID preserves per-customer order while letting SQS deliver different groups concurrently, which is how you keep parallelism. Standard queues offer best-effort ordering and at-least-once delivery, so neither the ordering nor the duplicate requirement is met, whatever the visibility timeout or polling mode. Option d serialises the entire queue to a single group and abandons the deduplication requirement."),
  de=("Ein Zahlungsablauf verlangt, dass Nachrichten je Kunde exakt in der Sendereihenfolge verarbeitet werden, dass eine Doppeleinreichung innerhalb des Deduplizierungsintervalls nicht zweimal verarbeitet wird und dass verschiedene Kunden dennoch parallel verarbeitet werden können. Welche Amazon-SQS-Konfiguration erfüllt das?",
      ["Eine Standard-Warteschlange mit einem Sichtbarkeits-Timeout, das länger als die Verarbeitungsdauer ist",
       "Eine Standard-Warteschlange mit aktiviertem Long Polling",
       "Eine FIFO-Warteschlange, die die Kundenkennung als Message Group ID verwendet, mit aktivierter inhaltsbasierter Deduplizierung",
       "Eine FIFO-Warteschlange mit allen Nachrichten in einer einzigen Nachrichtengruppe und deaktivierter Deduplizierung"],
      "FIFO-Warteschlangen garantieren die Reihenfolge innerhalb einer Nachrichtengruppe und eine Exactly-once-Verarbeitung innerhalb des fünfminütigen Deduplizierungsintervalls. Die Kundenkennung als Message Group ID erhält die Reihenfolge je Kunde und erlaubt SQS zugleich, verschiedene Gruppen nebenläufig zuzustellen - so bleibt die Parallelität erhalten. Standard-Warteschlangen bieten nur Best-Effort-Reihenfolge und At-least-once-Zustellung; damit ist weder die Reihenfolge- noch die Duplikatanforderung erfüllt, unabhängig von Sichtbarkeits-Timeout oder Abfragemodus. Antwort d serialisiert die gesamte Warteschlange und gibt die Deduplizierung auf."),
  ja=("ある決済ワークフローでは、同一顧客のメッセージが送信された順序どおりに処理されること、重複排除期間内の重複送信が二重処理されないこと、それでも異なる顧客どうしは並列に処理できることが求められます。この要件を満たす Amazon SQS の構成はどれですか。",
      ["処理時間より長い可視性タイムアウトを設定した標準キュー",
       "ロングポーリングを有効にした標準キュー",
       "顧客識別子をメッセージグループ ID として使い、コンテンツベースの重複排除を有効にした FIFO キュー",
       "すべてのメッセージを 1 つのメッセージグループに入れ、重複排除を無効にした FIFO キュー"],
      "FIFO キューは、メッセージグループ内での順序保証と、5 分間の重複排除期間内での 1 回限りの処理を保証します。顧客識別子をメッセージグループ ID にすれば、顧客ごとの順序を保ちながら、異なるグループを同時に配信できるため並列性も維持できます。標準キューはベストエフォートの順序と最低 1 回の配信であり、可視性タイムアウトやポーリング方式に関わらず順序要件も重複要件も満たしません。選択肢 d はキュー全体を 1 グループに直列化し、重複排除の要件も放棄しています。"),
  zh=("某支付流程要求：同一客户的消息必须严格按发送顺序处理；重复数据删除窗口内的重复提交不得被处理两次；同时不同客户之间仍可并行处理。哪种 Amazon SQS 配置能满足这些要求？",
      ["可见性超时长于处理时间的标准队列",
       "启用了长轮询的标准队列",
       "以客户标识作为消息组 ID、并启用基于内容的重复数据删除的 FIFO 队列",
       "将所有消息放入单个消息组、并禁用重复数据删除的 FIFO 队列"],
      "FIFO 队列保证消息组内部的顺序，并在 5 分钟的重复数据删除窗口内保证仅处理一次。用客户标识作为消息组 ID，可在保持每个客户内部顺序的同时，让 SQS 并发投递不同的组，从而保留并行度。标准队列只提供尽力而为的顺序和至少一次投递，无论可见性超时或轮询方式如何，都无法满足顺序与去重要求。选项 d 把整个队列串行化为一个组，并放弃了去重要求。"))

Q("aws-saa-resilient-07", "resilient_architectures",
  "Domain 2, Task Statement 2.2 (Design highly available and/or fault-tolerant architectures)",
  True, False, SC, ["b"],
  "docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Replication.html",
  en=("Which statement about Amazon Aurora Replicas is correct?",
      ["Each Aurora Replica keeps its own independent copy of the data, asynchronously copied from the writer instance",
       "An Aurora DB cluster can contain up to 15 Aurora Replicas; they read from the same shared cluster volume as the writer and one is promoted automatically if the writer becomes unavailable",
       "Aurora Replicas can only be used as failover targets and cannot serve read queries",
       "Aurora Replicas must be created in the same Availability Zone as the writer instance"],
      "Aurora separates compute from a shared, distributed storage volume: the writer and all readers see the same cluster volume as a single logical volume, so there is no per-replica copy to keep in sync. AWS documents a maximum of 15 Aurora Replicas per cluster, states that they serve read queries to scale reads, and that Aurora automatically promotes a reader if the writer becomes unavailable. Replicas can and should be spread across Availability Zones, which is what makes them useful for availability."),
  de=("Welche Aussage über Amazon Aurora Replicas ist richtig?",
      ["Jedes Aurora Replica hält eine eigene, unabhängige Kopie der Daten, die asynchron von der Writer-Instanz kopiert wird",
       "Ein Aurora-DB-Cluster kann bis zu 15 Aurora Replicas enthalten; sie lesen dasselbe gemeinsame Cluster-Volume wie der Writer, und eines wird automatisch befördert, wenn der Writer ausfällt",
       "Aurora Replicas können nur als Failover-Ziele dienen und keine Leseabfragen bedienen",
       "Aurora Replicas müssen in derselben Availability Zone wie die Writer-Instanz angelegt werden"],
      "Aurora trennt Rechenleistung von einem gemeinsamen, verteilten Speicher-Volume: Writer und alle Reader sehen dasselbe Cluster-Volume als ein einziges logisches Volume, es gibt also keine je Replikat zu synchronisierende Kopie. AWS dokumentiert höchstens 15 Aurora Replicas je Cluster, dass sie Leseabfragen zur Skalierung bedienen und dass Aurora bei Ausfall des Writers automatisch einen Reader befördert. Replicas können und sollen über Availability Zones verteilt werden - genau das macht sie für die Verfügbarkeit nützlich."),
  ja=("Amazon Aurora レプリカに関する記述として正しいものはどれですか。",
      ["各 Aurora レプリカは独自の独立したデータのコピーを保持し、ライターインスタンスから非同期にコピーされる",
       "Aurora DB クラスターは最大 15 個の Aurora レプリカを持てる。レプリカはライターと同じ共有クラスターボリュームを読み、ライターが利用不能になると自動的に 1 つが昇格する",
       "Aurora レプリカはフェイルオーバー先としてのみ使え、読み取りクエリは処理できない",
       "Aurora レプリカはライターインスタンスと同じアベイラビリティーゾーンに作成しなければならない"],
      "Aurora はコンピューティングと共有分散ストレージボリュームを分離しています。ライターとすべてのリーダーは同じクラスターボリュームを 1 つの論理ボリュームとして参照するため、レプリカごとに同期すべきコピーは存在しません。AWS はクラスターあたり最大 15 個の Aurora レプリカ、読み取りスケーリングのためのクエリ処理、ライター障害時のリーダー自動昇格を明記しています。レプリカはアベイラビリティーゾーンをまたいで配置でき、またそうすべきです。それこそが可用性に寄与する理由です。"),
  zh=("关于 Amazon Aurora 副本，下列哪项说法正确？",
      ["每个 Aurora 副本都保存自己独立的一份数据，由写入器实例异步复制而来",
       "一个 Aurora 数据库集群最多可包含 15 个 Aurora 副本；它们与写入器读取同一个共享集群卷，写入器不可用时会自动提升其中一个",
       "Aurora 副本只能用作故障转移目标，不能处理读取查询",
       "Aurora 副本必须与写入器实例位于同一个可用区"],
      "Aurora 将计算与共享的分布式存储卷分离：写入器和所有读取器把同一个集群卷视为单一逻辑卷，因此不存在需要逐副本同步的数据副本。AWS 文档说明每个集群最多 15 个 Aurora 副本，它们可处理读取查询以扩展读能力，并且写入器不可用时 Aurora 会自动提升某个读取器。副本可以且应当跨可用区分布，这正是它们对可用性有价值的原因。"))

Q("aws-saa-resilient-08", "resilient_architectures",
  "Domain 2, Task Statement 2.2 (Design highly available and/or fault-tolerant architectures)",
  True, True, MC, ["b", "d"],
  "docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html and docs.aws.amazon.com/autoscaling/ec2/userguide/auto-scaling-benefits.html",
  en=("A stateless web application runs on two EC2 instances in one Availability Zone behind an Application Load Balancer. Which TWO changes make it tolerant of the loss of an entire Availability Zone?",
      ["Increase the instance type from m5.large to m5.4xlarge",
       "Enable the load balancer in subnets in at least two Availability Zones",
       "Enable termination protection on both instances",
       "Configure the Auto Scaling group to span subnets in those Availability Zones, with a minimum capacity of at least two",
       "Attach a second Elastic IP address to each instance"],
      "An Application Load Balancer places a node in each enabled Availability Zone and only routes to targets in zones it is enabled in, so it must be enabled in at least two. The Auto Scaling group must in turn be allowed to launch and rebalance capacity across those zones and must keep enough instances running that the loss of one zone still leaves capacity. Vertical scaling makes one instance bigger in the same zone. Termination protection prevents an API call, not a zone failure. Extra Elastic IPs change nothing about availability."),
  de=("Eine zustandslose Webanwendung läuft auf zwei EC2-Instanzen in einer Availability Zone hinter einem Application Load Balancer. Welche ZWEI Änderungen machen sie gegen den Ausfall einer ganzen Availability Zone widerstandsfähig?",
      ["Den Instanztyp von m5.large auf m5.4xlarge vergrößern",
       "Den Load Balancer in Subnetzen in mindestens zwei Availability Zones aktivieren",
       "Den Terminierungsschutz für beide Instanzen aktivieren",
       "Die Auto-Scaling-Gruppe über die Subnetze dieser Availability Zones spannen, mit einer Mindestkapazität von mindestens zwei",
       "Jeder Instanz eine zweite Elastic IP zuweisen"],
      "Ein Application Load Balancer betreibt in jeder aktivierten Availability Zone einen Knoten und leitet nur an Ziele in aktivierten Zonen weiter; er muss also in mindestens zwei Zonen aktiviert sein. Die Auto-Scaling-Gruppe wiederum muss Kapazität über diese Zonen starten und ausbalancieren dürfen und genügend Instanzen halten, damit nach dem Verlust einer Zone noch Kapazität übrig ist. Vertikale Skalierung macht eine Instanz in derselben Zone nur größer. Terminierungsschutz verhindert einen API-Aufruf, keinen Zonenausfall. Zusätzliche Elastic IPs ändern an der Verfügbarkeit nichts."),
  ja=("ステートレスなウェブアプリケーションが、Application Load Balancer の背後にある単一アベイラビリティーゾーン内の 2 台の EC2 インスタンスで稼働しています。アベイラビリティーゾーン全体の障害に耐えられるようにする変更は、どの 2 つですか。",
      ["インスタンスタイプを m5.large から m5.4xlarge に変更する",
       "ロードバランサーを少なくとも 2 つのアベイラビリティーゾーンのサブネットで有効にする",
       "両方のインスタンスで終了保護を有効にする",
       "Auto Scaling グループをそれらのアベイラビリティーゾーンのサブネットにまたがるよう構成し、最小キャパシティを 2 以上にする",
       "各インスタンスに 2 つ目の Elastic IP アドレスをアタッチする"],
      "Application Load Balancer は有効化された各アベイラビリティーゾーンにノードを配置し、有効化されたゾーン内のターゲットにのみルーティングします。したがって最低 2 ゾーンで有効化する必要があります。さらに Auto Scaling グループがそれらのゾーンにまたがって起動・再配置でき、1 ゾーンを失っても容量が残るだけのインスタンス数を維持する必要があります。垂直スケーリングは同じゾーン内のインスタンスを大きくするだけです。終了保護が防ぐのは API 呼び出しであってゾーン障害ではありません。Elastic IP を追加しても可用性は変わりません。"),
  zh=("某无状态 Web 应用运行在单个可用区内的两台 EC2 实例上，前面是一个 Application Load Balancer。哪两项变更能使其容忍整个可用区的故障？",
      ["将实例类型由 m5.large 提升为 m5.4xlarge",
       "在至少两个可用区的子网中启用该负载均衡器",
       "为两台实例启用终止保护",
       "将 Auto Scaling 组配置为跨这些可用区的子网，并把最小容量设为至少 2",
       "为每台实例再附加一个弹性 IP 地址"],
      "Application Load Balancer 会在每个已启用的可用区中部署一个节点，并且只把流量路由到已启用可用区中的目标，因此必须至少在两个可用区中启用。Auto Scaling 组也必须被允许跨这些可用区启动和再平衡容量，并保持足够的实例数量，使得损失一个可用区后仍有可用容量。纵向扩容只是把同一可用区里的实例变大。终止保护阻止的是 API 调用，而不是可用区故障。额外的弹性 IP 对可用性没有任何帮助。"))

Q("aws-saa-resilient-09", "resilient_architectures",
  "Domain 2, Task Statement 2.1 (Design scalable and loosely coupled architectures)",
  False, False, SC, ["d"],
  "docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html",
  en=("A small number of malformed messages in an Amazon SQS queue are received, fail processing, return to the queue after the visibility timeout, and are received again, holding up throughput. What is the standard remedy?",
      ["Reduce the visibility timeout so that the messages are retried sooner",
       "Enable long polling on the queue",
       "Convert the queue from standard to FIFO",
       "Configure a redrive policy with a dead-letter queue and a maxReceiveCount, so that repeatedly failing messages are moved aside automatically"],
      "A dead-letter queue with a maxReceiveCount is the designed answer to poison messages: after the configured number of unsuccessful receives, SQS moves the message to the DLQ where it can be inspected without blocking the main queue. Shortening the visibility timeout makes the loop tighter, not better. Long polling reduces empty ReceiveMessage responses and has nothing to do with failures. Converting to FIFO changes ordering and deduplication semantics, not failure handling."),
  de=("Einige wenige fehlerhafte Nachrichten in einer Amazon-SQS-Warteschlange werden empfangen, scheitern bei der Verarbeitung, kehren nach dem Sichtbarkeits-Timeout in die Warteschlange zurück und werden erneut empfangen - das bremst den Durchsatz. Was ist das übliche Gegenmittel?",
      ["Das Sichtbarkeits-Timeout verkürzen, damit die Nachrichten früher erneut versucht werden",
       "Long Polling für die Warteschlange aktivieren",
       "Die Warteschlange von Standard auf FIFO umstellen",
       "Eine Redrive-Richtlinie mit Dead-Letter-Queue und maxReceiveCount konfigurieren, sodass wiederholt scheiternde Nachrichten automatisch beiseitegelegt werden"],
      "Eine Dead-Letter-Queue mit maxReceiveCount ist die vorgesehene Antwort auf Poison Messages: Nach der eingestellten Zahl erfolgloser Empfänge verschiebt SQS die Nachricht in die DLQ, wo sie untersucht werden kann, ohne die Hauptwarteschlange zu blockieren. Ein kürzeres Sichtbarkeits-Timeout macht die Schleife nur enger. Long Polling verringert leere ReceiveMessage-Antworten und hat mit Fehlern nichts zu tun. Die Umstellung auf FIFO ändert Reihenfolge und Deduplizierung, nicht die Fehlerbehandlung."),
  ja=("Amazon SQS キュー内のわずかな不正メッセージが受信され、処理に失敗し、可視性タイムアウト後にキューへ戻り、再び受信される、という繰り返しでスループットが低下しています。標準的な対処はどれですか。",
      ["可視性タイムアウトを短くして、より早く再試行させる",
       "キューでロングポーリングを有効にする",
       "キューを標準から FIFO に変換する",
       "デッドレターキューと maxReceiveCount を持つリドライブポリシーを構成し、繰り返し失敗するメッセージを自動的に隔離する"],
      "maxReceiveCount を伴うデッドレターキューは、いわゆるポイズンメッセージに対する本来の解決策です。設定回数だけ受信に失敗すると、SQS はそのメッセージを DLQ へ移動し、メインキューを塞ぐことなく調査できます。可視性タイムアウトを短くしてもループが速くなるだけです。ロングポーリングは空の ReceiveMessage 応答を減らすもので、失敗とは無関係です。FIFO への変換は順序と重複排除の意味論を変えるだけで、失敗処理は変わりません。"),
  zh=("Amazon SQS 队列中少量格式错误的消息被接收、处理失败，在可见性超时后回到队列并被再次接收，从而拖慢吞吐量。标准的处理办法是什么？",
      ["缩短可见性超时，使这些消息更快被重试",
       "为该队列启用长轮询",
       "把队列从标准队列转换为 FIFO 队列",
       "配置带死信队列和 maxReceiveCount 的重新驱动策略，使反复失败的消息被自动移出"],
      "带 maxReceiveCount 的死信队列正是针对“毒消息”的既定解决方案：在配置的失败接收次数之后，SQS 会把该消息移到死信队列，可在不阻塞主队列的情况下进行排查。缩短可见性超时只会让循环更快，并不会更好。长轮询减少的是空的 ReceiveMessage 响应，与失败无关。转换为 FIFO 改变的是顺序与去重语义，而不是失败处理。"))

# ==========================================================================
# Domain 3 - Design High-Performing Architectures (24% of scored) - 9 Q
# ==========================================================================

Q("aws-saa-performance-01", "high_performing_architectures",
  "Domain 3, Task Statement 3.1 (Determine high-performing and/or scalable storage solutions)",
  True, False, SC, ["c"],
  "docs.aws.amazon.com/efs/latest/ug/how-it-works.html and docs.aws.amazon.com/ebs/latest/userguide/ebs-volumes.html",
  en=("A content-management application runs on an Auto Scaling group spread across three Availability Zones. Every instance must read and write the same set of files using standard POSIX file semantics. Which storage service should be used?",
      ["An Amazon EBS gp3 volume attached to each instance",
       "An EC2 instance store volume on each instance",
       "Amazon EFS, mounted by all instances through mount targets in each Availability Zone",
       "An Amazon S3 bucket mounted as a block device on each instance"],
      "Amazon EFS is a managed NFS file system with a mount target in each Availability Zone, so instances in all three zones read and write one shared file system with POSIX semantics. An EBS volume is zonal and, outside io1/io2 Multi-Attach within a single zone, attaches to one instance at a time, so each instance would get its own separate copy of the data. Instance store is ephemeral and node-local: it disappears when the instance stops. S3 is object storage and is not a block device."),
  de=("Eine Content-Management-Anwendung läuft in einer Auto-Scaling-Gruppe über drei Availability Zones. Jede Instanz muss dieselben Dateien mit gewöhnlicher POSIX-Dateisemantik lesen und schreiben. Welcher Speicherdienst ist zu verwenden?",
      ["Ein an jede Instanz angehängtes Amazon-EBS-gp3-Volume",
       "Ein EC2-Instance-Store-Volume auf jeder Instanz",
       "Amazon EFS, von allen Instanzen über Mount-Targets in jeder Availability Zone eingehängt",
       "Ein als Blockgerät eingehängter Amazon-S3-Bucket auf jeder Instanz"],
      "Amazon EFS ist ein verwaltetes NFS-Dateisystem mit einem Mount-Target je Availability Zone; Instanzen aller drei Zonen lesen und schreiben also ein gemeinsames Dateisystem mit POSIX-Semantik. Ein EBS-Volume ist zonal und - außerhalb von io1/io2-Multi-Attach innerhalb einer Zone - jeweils an eine Instanz angehängt, sodass jede Instanz ihre eigene Kopie der Daten hätte. Instance Store ist flüchtig und knotenlokal: Er verschwindet, wenn die Instanz gestoppt wird. S3 ist Objektspeicher und kein Blockgerät."),
  ja=("コンテンツ管理アプリケーションが、3 つのアベイラビリティーゾーンにまたがる Auto Scaling グループ上で動作しています。すべてのインスタンスが、標準的な POSIX ファイルセマンティクスで同じファイル群を読み書きする必要があります。どのストレージサービスを使うべきですか。",
      ["各インスタンスにアタッチした Amazon EBS gp3 ボリューム",
       "各インスタンスの EC2 インスタンスストアボリューム",
       "各アベイラビリティーゾーンのマウントターゲット経由で全インスタンスがマウントする Amazon EFS",
       "各インスタンスにブロックデバイスとしてマウントした Amazon S3 バケット"],
      "Amazon EFS は各アベイラビリティーゾーンにマウントターゲットを持つマネージド NFS ファイルシステムであり、3 ゾーンすべてのインスタンスが POSIX セマンティクスで 1 つの共有ファイルシステムを読み書きできます。EBS ボリュームはゾーン単位であり、単一ゾーン内の io1/io2 マルチアタッチを除けば一度に 1 インスタンスにしかアタッチできないため、各インスタンスが別々のデータコピーを持つことになります。インスタンスストアは揮発性かつノードローカルで、インスタンスを停止すると消えます。S3 はオブジェクトストレージであり、ブロックデバイスではありません。"),
  zh=("某内容管理应用运行在跨三个可用区的 Auto Scaling 组上。所有实例都必须使用标准 POSIX 文件语义读写同一组文件。应使用哪种存储服务？",
      ["为每台实例各挂载一个 Amazon EBS gp3 卷",
       "每台实例上的 EC2 实例存储卷",
       "Amazon EFS，由所有实例通过各可用区的挂载目标进行挂载",
       "把 Amazon S3 存储桶作为块设备挂载到每台实例"],
      "Amazon EFS 是托管的 NFS 文件系统，在每个可用区都有挂载目标，因此三个可用区中的实例可以用 POSIX 语义读写同一个共享文件系统。EBS 卷是可用区级的，除了单可用区内的 io1/io2 多重挂载外，同一时刻只能挂载到一台实例，这样每台实例会各自拥有一份独立数据。实例存储是临时且节点本地的，实例停止后即消失。S3 是对象存储，不是块设备。"))

Q("aws-saa-performance-02", "high_performing_architectures",
  "Domain 3, Task Statement 3.1 (Determine high-performing and/or scalable storage solutions)",
  False, False, SC, ["b"],
  "docs.aws.amazon.com/ebs/latest/userguide/general-purpose.html",
  en=("A 200 GiB gp2 volume backing a database performs well for the first part of each morning and then slows sharply. The workload needs a sustained 6,000 IOPS. What is the most cost-effective fix?",
      ["Convert the volume to a magnetic (standard) volume, which has no credit system",
       "Convert the volume to gp3 and provision 6,000 IOPS",
       "Grow the gp2 volume to 2,000 GiB so that its baseline reaches 6,000 IOPS",
       "Move the database files onto an EC2 instance store volume"],
      "The symptom is gp2 burst-credit exhaustion. gp2 baseline IOPS scale at 3 IOPS per GiB, so a 200 GiB volume has a 600 IOPS baseline and bursts to 3,000 until its credits run out. gp3 decouples performance from capacity: it includes 3,000 IOPS and 125 MiB/s at any size, lets you provision more, and AWS states gp3 volumes do not use burst performance and can indefinitely sustain their provisioned level. Option c does reach 6,000 baseline IOPS but forces you to pay for 1.8 TiB of unused capacity. Magnetic volumes are slower still, and instance store data is lost when the instance stops."),
  de=("Ein 200-GiB-gp2-Volume unter einer Datenbank arbeitet jeden Morgen zunächst gut und wird dann deutlich langsamer. Die Last benötigt dauerhaft 6.000 IOPS. Was ist die wirtschaftlichste Lösung?",
      ["Das Volume in ein magnetisches (Standard-)Volume umwandeln, das kein Guthabensystem hat",
       "Das Volume auf gp3 umstellen und 6.000 IOPS bereitstellen",
       "Das gp2-Volume auf 2.000 GiB vergrößern, damit sein Grundwert 6.000 IOPS erreicht",
       "Die Datenbankdateien auf ein EC2-Instance-Store-Volume verschieben"],
      "Das Symptom ist der Verbrauch der gp2-Burst-Guthaben. Der gp2-Grundwert skaliert mit 3 IOPS je GiB; ein 200-GiB-Volume hat also 600 Basis-IOPS und burstet auf 3.000, bis die Guthaben aufgebraucht sind. gp3 entkoppelt Leistung von Kapazität: 3.000 IOPS und 125 MiB/s sind bei jeder Größe enthalten, mehr lässt sich bereitstellen, und laut AWS nutzen gp3-Volumes keine Burst-Leistung und halten ihr bereitgestelltes Niveau dauerhaft. Antwort c erreicht zwar 6.000 Basis-IOPS, zwingt aber zur Bezahlung von 1,8 TiB ungenutzter Kapazität. Magnetische Volumes sind noch langsamer, und Instance-Store-Daten gehen beim Stoppen der Instanz verloren."),
  ja=("データベースを支える 200 GiB の gp2 ボリュームが、毎朝しばらくは快調でその後急激に遅くなります。ワークロードには持続的に 6,000 IOPS が必要です。最も費用対効果の高い対処はどれですか。",
      ["クレジット方式のないマグネティック(standard)ボリュームに変換する",
       "ボリュームを gp3 に変換し、6,000 IOPS をプロビジョニングする",
       "gp2 ボリュームを 2,000 GiB に拡張し、ベースラインを 6,000 IOPS にする",
       "データベースファイルを EC2 インスタンスストアボリュームへ移動する"],
      "症状は gp2 のバーストクレジット枯渇です。gp2 のベースライン IOPS は 1 GiB あたり 3 IOPS で増えるため、200 GiB では 600 IOPS がベースラインで、クレジットが尽きるまで 3,000 IOPS にバーストします。gp3 は性能と容量を切り離し、サイズにかかわらず 3,000 IOPS と 125 MiB/s を含み、追加のプロビジョニングも可能です。AWS は gp3 がバースト性能を使わず、プロビジョニングした性能を無期限に維持できると明記しています。選択肢 c でもベースライン 6,000 IOPS には達しますが、使わない 1.8 TiB 分の容量を支払うことになります。マグネティックはさらに遅く、インスタンスストアはインスタンス停止でデータを失います。"),
  zh=("承载数据库的 200 GiB gp2 卷每天上午一开始表现良好，随后急剧变慢。该工作负载需要持续 6,000 IOPS。最具成本效益的修复方式是什么？",
      ["将该卷转换为没有信用机制的磁介质（standard）卷",
       "将该卷转换为 gp3 并预配 6,000 IOPS",
       "把 gp2 卷扩容到 2,000 GiB，使其基线达到 6,000 IOPS",
       "把数据库文件迁移到 EC2 实例存储卷上"],
      "症状是 gp2 突发信用耗尽。gp2 基线 IOPS 按每 GiB 3 IOPS 线性增长，因此 200 GiB 卷的基线为 600 IOPS，在信用耗尽前可突发到 3,000。gp3 将性能与容量解耦：任何容量都包含 3,000 IOPS 和 125 MiB/s，并可额外预配；AWS 明确指出 gp3 卷不使用突发性能，可以无限期维持所预配的性能。选项 c 确实能把基线提升到 6,000 IOPS，但要为 1.8 TiB 用不到的容量付费。磁介质卷更慢，而实例存储的数据会在实例停止时丢失。"))

Q("aws-saa-performance-03", "high_performing_architectures",
  "Domain 3, Task Statement 3.3 (Determine high-performing database solutions)",
  False, False, SC, ["a"],
  "docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.html",
  en=("A DynamoDB-backed leaderboard is read far more often than it is written. The team needs its single-digit millisecond reads to become microsecond reads, with the smallest possible application change and no change to the data model. What should be added?",
      ["Amazon DynamoDB Accelerator (DAX)",
       "Amazon ElastiCache for Memcached in front of the application",
       "A DynamoDB global secondary index on the score attribute",
       "DynamoDB Streams with an AWS Lambda consumer"],
      "DAX is a write-through, DynamoDB API-compatible in-memory cache that AWS documents as delivering microsecond read latency; the application swaps in the DAX client and otherwise keeps its existing calls, so the change is minimal and the table design is untouched. ElastiCache would also cache, but the application has to populate, read and invalidate the cache itself. A global secondary index enables a different query pattern; it does not accelerate the reads already being made. Streams are a change-data-capture feature."),
  de=("Eine auf DynamoDB gestützte Bestenliste wird weit häufiger gelesen als geschrieben. Das Team möchte aus den einstelligen Millisekunden-Lesezugriffen Mikrosekunden machen - mit möglichst kleiner Anwendungsänderung und ohne das Datenmodell anzufassen. Was sollte ergänzt werden?",
      ["Amazon DynamoDB Accelerator (DAX)",
       "Amazon ElastiCache for Memcached vor der Anwendung",
       "Ein globaler Sekundärindex auf dem Attribut score",
       "DynamoDB Streams mit einem AWS-Lambda-Verbraucher"],
      "DAX ist ein Write-Through-Cache im Arbeitsspeicher, der die DynamoDB-API spricht; laut AWS liefert er Leselatenzen im Mikrosekundenbereich. Die Anwendung tauscht lediglich den Client aus und behält ihre bestehenden Aufrufe, das Tabellendesign bleibt unangetastet. ElastiCache würde ebenfalls zwischenspeichern, doch die Anwendung müsste den Cache selbst füllen, lesen und invalidieren. Ein globaler Sekundärindex ermöglicht ein anderes Abfragemuster, beschleunigt aber die bereits erfolgenden Lesezugriffe nicht. Streams sind eine Change-Data-Capture-Funktion."),
  ja=("DynamoDB を使ったリーダーボードは、書き込みよりはるかに読み取りが多いワークロードです。チームは、アプリケーションの変更を最小限に抑え、データモデルも変えずに、1 桁ミリ秒の読み取りをマイクロ秒にしたいと考えています。何を追加すべきですか。",
      ["Amazon DynamoDB Accelerator (DAX)",
       "アプリケーションの前段に置く Amazon ElastiCache for Memcached",
       "score 属性に対する DynamoDB のグローバルセカンダリインデックス",
       "AWS Lambda コンシューマーを伴う DynamoDB Streams"],
      "DAX はライトスルー方式で DynamoDB API 互換のインメモリキャッシュであり、AWS はマイクロ秒級の読み取りレイテンシーを提供すると記載しています。アプリケーションは DAX クライアントに差し替えるだけで既存の呼び出しをそのまま使えるため、変更は最小限でテーブル設計にも手を入れません。ElastiCache でもキャッシュはできますが、投入・読み出し・無効化をアプリケーション自身が実装する必要があります。グローバルセカンダリインデックスは別のクエリパターンを可能にするもので、既存の読み取りを高速化するものではありません。Streams は変更データキャプチャの機能です。"),
  zh=("某基于 DynamoDB 的排行榜读取远多于写入。团队希望在应用改动最小、且不改变数据模型的前提下，把个位数毫秒级读取变为微秒级读取。应该增加什么？",
      ["Amazon DynamoDB Accelerator（DAX）",
       "在应用前面部署 Amazon ElastiCache for Memcached",
       "在 score 属性上创建 DynamoDB 全局二级索引",
       "配合 AWS Lambda 消费者使用 DynamoDB Streams"],
      "DAX 是直写式、兼容 DynamoDB API 的内存缓存，AWS 文档说明其可提供微秒级读取延迟；应用只需换用 DAX 客户端，其余调用保持不变，因此改动极小且表设计原封不动。ElastiCache 同样可以缓存，但需要应用自行负责填充、读取和失效处理。全局二级索引启用的是另一种查询模式，并不会加速现有读取。Streams 属于变更数据捕获功能。"))

Q("aws-saa-performance-04", "high_performing_architectures",
  "Domain 3, Task Statement 3.4 (Determine high-performing and/or scalable network architectures)",
  False, False, SC, ["d"],
  "docs.aws.amazon.com/global-accelerator/latest/dg/what-is-global-accelerator.html",
  en=("A multiplayer game exposes a UDP endpoint in two AWS Regions. Players worldwide need the lowest achievable latency, fixed IP addresses that can be built into the game client, and fast failover between Regions. Which service should front the endpoints?",
      ["Amazon CloudFront with the Regional endpoints as custom origins",
       "Amazon Route 53 latency-based routing on its own",
       "An internet-facing Application Load Balancer in each Region",
       "AWS Global Accelerator with both Regional endpoints registered in endpoint groups"],
      "Global Accelerator provides two static anycast IPv4 addresses from the AWS edge network (four addresses for dual-stack), moves traffic onto the AWS global network at the nearest edge location, supports TCP and UDP, and shifts traffic between endpoint groups when an endpoint becomes unhealthy. CloudFront is an HTTP(S) content delivery network and does not proxy arbitrary UDP. Route 53 alone depends on DNS caching and TTLs for failover and provides no fixed IPs. An ALB is Regional, layer 7 and addressed by DNS name, not by a static IP."),
  de=("Ein Mehrspieler-Spiel stellt einen UDP-Endpunkt in zwei AWS-Regionen bereit. Spieler weltweit brauchen die geringstmögliche Latenz, feste IP-Adressen, die sich in den Client einbauen lassen, und ein schnelles Umschalten zwischen den Regionen. Welcher Dienst gehört vor die Endpunkte?",
      ["Amazon CloudFront mit den regionalen Endpunkten als Custom Origins",
       "Amazon Route 53 mit latenzbasiertem Routing allein",
       "Je Region ein internetseitiger Application Load Balancer",
       "AWS Global Accelerator mit beiden regionalen Endpunkten in Endpunktgruppen"],
      "Global Accelerator stellt zwei statische Anycast-IPv4-Adressen aus dem AWS-Edge-Netz bereit (vier Adressen im Dual-Stack-Betrieb), holt den Verkehr am nächstgelegenen Edge-Standort ins globale AWS-Netz, unterstützt TCP und UDP und verlagert den Verkehr zwischen Endpunktgruppen, sobald ein Endpunkt ungesund wird. CloudFront ist ein HTTP(S)-Content-Delivery-Netzwerk und leitet kein beliebiges UDP weiter. Route 53 allein hängt beim Umschalten an DNS-Caching und TTLs und liefert keine festen IPs. Ein ALB ist regional, arbeitet auf Schicht 7 und wird über einen DNS-Namen adressiert, nicht über eine statische IP."),
  ja=("あるマルチプレイヤーゲームが、2 つの AWS リージョンで UDP エンドポイントを公開しています。世界中のプレイヤーに対して可能な限り低いレイテンシー、ゲームクライアントに組み込める固定 IP アドレス、そしてリージョン間の高速なフェイルオーバーが必要です。エンドポイントの前段に置くべきサービスはどれですか。",
      ["リージョナルエンドポイントをカスタムオリジンとする Amazon CloudFront",
       "Amazon Route 53 のレイテンシーベースルーティング単体",
       "各リージョンにインターネット向け Application Load Balancer を配置する",
       "両方のリージョナルエンドポイントをエンドポイントグループに登録した AWS Global Accelerator"],
      "Global Accelerator は AWS エッジネットワークから 2 つの静的 Anycast IPv4 アドレス(デュアルスタックでは計 4 アドレス)を提供し、最寄りのエッジロケーションでトラフィックを AWS グローバルネットワークに載せ、TCP と UDP をサポートし、エンドポイントが異常になるとエンドポイントグループ間でトラフィックを切り替えます。CloudFront は HTTP(S) の CDN であり、任意の UDP をプロキシしません。Route 53 単体ではフェイルオーバーが DNS キャッシュと TTL に依存し、固定 IP も得られません。ALB はリージョナルかつレイヤー 7 で、静的 IP ではなく DNS 名でアドレス指定されます。"),
  zh=("某多人游戏在两个 AWS 区域各暴露一个 UDP 终端节点。全球玩家需要尽可能低的延迟、可写入游戏客户端的固定 IP 地址，以及区域之间的快速故障转移。应在终端节点前面使用哪项服务？",
      ["以区域终端节点作为自定义源站的 Amazon CloudFront",
       "仅使用 Amazon Route 53 基于延迟的路由",
       "在每个区域各部署一个面向互联网的 Application Load Balancer",
       "将两个区域终端节点注册到终端节点组的 AWS Global Accelerator"],
      "Global Accelerator 从 AWS 边缘网络提供两个静态任播 IPv4 地址（双栈情况下共四个地址），在最近的边缘站点将流量导入 AWS 全球网络，支持 TCP 和 UDP，并在终端节点不健康时在终端节点组之间切换流量。CloudFront 是 HTTP(S) 内容分发网络，不代理任意 UDP。仅靠 Route 53 时故障转移依赖 DNS 缓存与 TTL，且不提供固定 IP。ALB 是区域级的第 7 层服务，通过 DNS 名称而非静态 IP 寻址。"))

Q("aws-saa-performance-05", "high_performing_architectures",
  "Domain 3, Task Statement 3.2 (Design high-performing and elastic compute solutions)",
  False, False, SC, ["b"],
  "docs.aws.amazon.com/lambda/latest/dg/provisioned-concurrency.html",
  en=("A latency-sensitive AWS Lambda function behind Amazon API Gateway occasionally responds slowly because of cold starts, especially after quiet periods. Which option addresses the cold starts most directly?",
      ["Increase the function's timeout setting",
       "Configure provisioned concurrency on a published version or alias of the function",
       "Increase the function's reserved concurrency",
       "Attach the function to a VPC"],
      "Provisioned concurrency keeps a chosen number of execution environments initialised and ready to respond, which is precisely the cold-start problem. The timeout governs how long an invocation may run before being stopped. Reserved concurrency caps and guarantees how many concurrent executions a function may have; it allocates a share of the account limit but does not pre-initialise anything. Attaching a function to a VPC does not reduce initialisation work and historically added to it."),
  de=("Eine latenzempfindliche AWS-Lambda-Funktion hinter Amazon API Gateway antwortet gelegentlich langsam - wegen Kaltstarts, besonders nach ruhigen Phasen. Welche Option adressiert die Kaltstarts am direktesten?",
      ["Das Timeout der Funktion erhöhen",
       "Provisioned Concurrency für eine veröffentlichte Version oder einen Alias der Funktion konfigurieren",
       "Die Reserved Concurrency der Funktion erhöhen",
       "Die Funktion an eine VPC anbinden"],
      "Provisioned Concurrency hält eine gewählte Anzahl von Ausführungsumgebungen initialisiert und antwortbereit - genau das Kaltstartproblem. Das Timeout regelt, wie lange ein Aufruf laufen darf, bevor er abgebrochen wird. Reserved Concurrency begrenzt und garantiert die Zahl gleichzeitiger Ausführungen; sie reserviert einen Anteil des Kontolimits, initialisiert aber nichts im Voraus. Eine VPC-Anbindung verringert die Initialisierungsarbeit nicht und erhöhte sie historisch sogar."),
  ja=("Amazon API Gateway の背後にあるレイテンシー重視の AWS Lambda 関数が、特に閑散時間の後にコールドスタートで遅くなることがあります。コールドスタートに最も直接的に対処する選択肢はどれですか。",
      ["関数のタイムアウト設定を大きくする",
       "関数の公開バージョンまたはエイリアスに対してプロビジョニング済み同時実行を設定する",
       "関数の予約済み同時実行数を増やす",
       "関数を VPC に接続する"],
      "プロビジョニング済み同時実行は、指定した数の実行環境を初期化済みかつ応答可能な状態で維持するもので、まさにコールドスタートへの対策です。タイムアウトは 1 回の呼び出しが停止されるまでの実行可能時間を決めるだけです。予約済み同時実行は同時実行数の上限を定めて確保するもので、アカウント上限の一部を割り当てはしますが事前初期化は行いません。VPC への接続は初期化処理を減らさず、歴史的にはむしろ増やしていました。"),
  zh=("位于 Amazon API Gateway 之后、对延迟敏感的 AWS Lambda 函数偶尔会因冷启动而响应缓慢，尤其是在低流量时段之后。哪个选项最直接地解决冷启动问题？",
      ["调大函数的超时设置",
       "为该函数的已发布版本或别名配置预置并发",
       "提高该函数的预留并发",
       "把该函数接入 VPC"],
      "预置并发会保持指定数量的执行环境处于已初始化、可立即响应的状态，正是针对冷启动问题。超时设置决定的是单次调用被终止前可运行多久。预留并发用于限制并保证函数的并发执行数量，它从账户配额中划出一部分，但不会预先初始化任何环境。把函数接入 VPC 不会减少初始化工作，历史上反而会增加。"))

Q("aws-saa-performance-06", "high_performing_architectures",
  "Domain 3, Task Statement 3.5 (Determine high-performing data ingestion and transformation solutions)",
  True, False, SC, ["c"],
  "docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html",
  en=("Clickstream events must land in Amazon S3 in near real time, converted to Apache Parquet, with no shards or servers for the team to manage. There is no requirement to replay the stream or to have several independent consumers. Which service fits best?",
      ["Amazon Kinesis Data Streams with a custom consumer application",
       "Amazon SQS with an AWS Lambda consumer that writes the objects",
       "Amazon Data Firehose delivering to the S3 bucket, with record format conversion enabled",
       "AWS DataSync"],
      "Firehose is the fully managed delivery stream: it buffers by size or time, can convert incoming records to Parquet or ORC, and writes to S3 without any shard management. Kinesis Data Streams gives retention, replay and multiple independent consumers, but the scenario explicitly does not need those and you must then manage capacity and write the consumer. SQS is a message queue with no S3 delivery and no format conversion. DataSync moves files between file and object stores; it is not an event-ingestion service."),
  de=("Clickstream-Ereignisse sollen nahezu in Echtzeit in Amazon S3 landen, in Apache Parquet umgewandelt, ohne dass das Team Shards oder Server verwalten muss. Ein Wiederabspielen des Streams oder mehrere unabhängige Verbraucher sind nicht gefordert. Welcher Dienst passt am besten?",
      ["Amazon Kinesis Data Streams mit einer eigenen Verbraucheranwendung",
       "Amazon SQS mit einem AWS-Lambda-Verbraucher, der die Objekte schreibt",
       "Amazon Data Firehose mit Zustellung in den S3-Bucket und aktivierter Datensatzformatkonvertierung",
       "AWS DataSync"],
      "Firehose ist der vollständig verwaltete Zustellungsstream: Er puffert nach Größe oder Zeit, kann eingehende Datensätze nach Parquet oder ORC konvertieren und schreibt ohne jede Shard-Verwaltung nach S3. Kinesis Data Streams bietet Aufbewahrung, Wiederabspielen und mehrere unabhängige Verbraucher - genau das braucht das Szenario ausdrücklich nicht, und man müsste Kapazität verwalten und den Verbraucher selbst schreiben. SQS ist eine Nachrichtenwarteschlange ohne S3-Zustellung und ohne Formatkonvertierung. DataSync verschiebt Dateien zwischen Datei- und Objektspeichern und ist kein Ereignis-Ingestionsdienst."),
  ja=("クリックストリームのイベントを、Apache Parquet に変換したうえでほぼリアルタイムに Amazon S3 へ配置する必要があります。シャードやサーバーの管理は避けたく、ストリームの再生や複数の独立したコンシューマーは不要です。最も適したサービスはどれですか。",
      ["独自のコンシューマーアプリケーションを伴う Amazon Kinesis Data Streams",
       "オブジェクトを書き込む AWS Lambda コンシューマーを伴う Amazon SQS",
       "レコード形式変換を有効にし、S3 バケットへ配信する Amazon Data Firehose",
       "AWS DataSync"],
      "Firehose は完全マネージドの配信ストリームです。サイズまたは時間でバッファリングし、受信レコードを Parquet や ORC に変換でき、シャード管理なしで S3 に書き込みます。Kinesis Data Streams は保持・再生・複数の独立コンシューマーを提供しますが、このシナリオではそれらが明示的に不要であり、その代わり容量管理とコンシューマー実装が必要になります。SQS はメッセージキューであり、S3 配信も形式変換も持ちません。DataSync はファイルストアとオブジェクトストア間でファイルを移動するもので、イベント取り込みサービスではありません。"),
  zh=("点击流事件需要近实时地写入 Amazon S3，并转换为 Apache Parquet 格式，同时团队不希望管理分片或服务器。无需重放流数据，也不需要多个相互独立的消费者。哪项服务最合适？",
      ["搭配自定义消费者应用的 Amazon Kinesis Data Streams",
       "搭配写入对象的 AWS Lambda 消费者的 Amazon SQS",
       "启用记录格式转换、直接投递到 S3 存储桶的 Amazon Data Firehose",
       "AWS DataSync"],
      "Firehose 是完全托管的投递流：它按大小或时间缓冲，可将传入记录转换为 Parquet 或 ORC，并在无需任何分片管理的情况下写入 S3。Kinesis Data Streams 提供保留、重放和多个独立消费者，但题目明确说明并不需要这些，反而要求你管理容量并自行编写消费者。SQS 是消息队列，既不提供 S3 投递也不提供格式转换。DataSync 用于在文件存储与对象存储之间搬运文件，不是事件摄取服务。"))

Q("aws-saa-performance-07", "high_performing_architectures",
  "Domain 3, Task Statement 3.1 (Determine high-performing and/or scalable storage solutions)",
  False, False, SC, ["a"],
  "docs.aws.amazon.com/fsx/latest/LustreGuide/what-is.html",
  en=("An HPC simulation cluster needs a shared file system with sub-millisecond latency and very high aggregate throughput, and it must process input data that already sits in an Amazon S3 bucket. Which service should be used?",
      ["Amazon FSx for Lustre, with a data repository association to the S3 bucket",
       "Amazon FSx for Windows File Server",
       "Amazon EFS in General Purpose performance mode",
       "Amazon S3 read directly over HTTPS from every compute node"],
      "FSx for Lustre is AWS's managed implementation of the Lustre parallel file system, built for HPC and machine learning: sub-millisecond latencies and throughput that scales with the file system's size. Its data repository association presents S3 objects as files, loads them lazily on first access and can export results back to the bucket. FSx for Windows File Server serves SMB workloads. EFS is NFS and does not reach Lustre's per-client throughput. Reading straight from S3 gives object semantics and far higher per-request latency."),
  de=("Ein HPC-Simulationscluster benötigt ein gemeinsames Dateisystem mit Latenzen unter einer Millisekunde und sehr hohem Gesamtdurchsatz und muss Eingabedaten verarbeiten, die bereits in einem Amazon-S3-Bucket liegen. Welcher Dienst ist zu verwenden?",
      ["Amazon FSx for Lustre mit einer Data-Repository-Verknüpfung zum S3-Bucket",
       "Amazon FSx for Windows File Server",
       "Amazon EFS im Leistungsmodus General Purpose",
       "Amazon S3, von jedem Rechenknoten direkt über HTTPS gelesen"],
      "FSx for Lustre ist die verwaltete AWS-Umsetzung des parallelen Dateisystems Lustre, gebaut für HPC und maschinelles Lernen: Latenzen unter einer Millisekunde und ein Durchsatz, der mit der Größe des Dateisystems skaliert. Die Data-Repository-Verknüpfung stellt S3-Objekte als Dateien dar, lädt sie beim ersten Zugriff nach und kann Ergebnisse zurück in den Bucket exportieren. FSx for Windows File Server bedient SMB-Lasten. EFS ist NFS und erreicht den Durchsatz je Client von Lustre nicht. Direkt aus S3 zu lesen liefert Objektsemantik und deutlich höhere Latenz je Anfrage."),
  ja=("HPC シミュレーションクラスターは、サブミリ秒のレイテンシーと非常に高い合計スループットを持つ共有ファイルシステムを必要とし、すでに Amazon S3 バケットにある入力データを処理する必要があります。どのサービスを使うべきですか。",
      ["S3 バケットへのデータリポジトリ関連付けを構成した Amazon FSx for Lustre",
       "Amazon FSx for Windows File Server",
       "汎用パフォーマンスモードの Amazon EFS",
       "各計算ノードから HTTPS で直接読み取る Amazon S3"],
      "FSx for Lustre は並列ファイルシステム Lustre の AWS マネージド実装で、HPC と機械学習向けに作られており、サブミリ秒のレイテンシーとファイルシステムサイズに応じて拡張するスループットを提供します。データリポジトリ関連付けにより S3 オブジェクトをファイルとして提示し、初回アクセス時に遅延ロードし、結果をバケットへ書き戻すこともできます。FSx for Windows File Server は SMB ワークロード向けです。EFS は NFS であり、Lustre のクライアントあたりスループットには届きません。S3 から直接読む方式はオブジェクトセマンティクスとなり、リクエストあたりのレイテンシーもはるかに高くなります。"),
  zh=("某 HPC 仿真集群需要一个具备亚毫秒延迟和极高聚合吞吐的共享文件系统，并且必须处理已经存放在 Amazon S3 存储桶中的输入数据。应使用哪项服务？",
      ["配置了到该 S3 存储桶的数据存储库关联的 Amazon FSx for Lustre",
       "Amazon FSx for Windows File Server",
       "通用性能模式的 Amazon EFS",
       "从每个计算节点直接通过 HTTPS 读取 Amazon S3"],
      "FSx for Lustre 是 AWS 对并行文件系统 Lustre 的托管实现，专为 HPC 和机器学习构建：亚毫秒级延迟，吞吐随文件系统规模扩展。其数据存储库关联可将 S3 对象呈现为文件、在首次访问时惰性加载，并可把结果导出回存储桶。FSx for Windows File Server 面向 SMB 工作负载。EFS 是 NFS，达不到 Lustre 的单客户端吞吐水平。直接从 S3 读取得到的是对象语义，且单请求延迟高得多。"))

Q("aws-saa-performance-08", "high_performing_architectures",
  "Domain 3, Task Statement 3.4 (Determine high-performing and/or scalable network architectures)",
  False, False, SC, ["d"],
  "docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html",
  en=("A hybrid application replicates several terabytes per day from an on-premises data centre into a VPC and is sensitive to jitter. The existing AWS Site-to-Site VPN over the public internet delivers inconsistent throughput. What should the architect recommend?",
      ["Add a second Site-to-Site VPN tunnel to the same virtual private gateway",
       "Enable enhanced networking on the instances in the VPC",
       "Route the replication traffic through a NAT gateway",
       "Provision AWS Direct Connect, optionally keeping the VPN as an encrypted backup path"],
      "Direct Connect is a dedicated private network connection between the customer's premises and AWS, which is what gives consistent bandwidth and latency for jitter-sensitive bulk transfer; keeping the VPN as a backup is the standard resilient hybrid design. A second VPN tunnel still rides the public internet and inherits the same variability. Enhanced networking affects packet performance inside the instance, not the wide-area path. A NAT gateway serves outbound traffic from private subnets and has nothing to do with inbound replication from on-premises."),
  de=("Eine hybride Anwendung repliziert täglich mehrere Terabyte aus einem lokalen Rechenzentrum in eine VPC und reagiert empfindlich auf Jitter. Das bestehende AWS Site-to-Site VPN über das öffentliche Internet liefert schwankenden Durchsatz. Was sollte empfohlen werden?",
      ["Einen zweiten Site-to-Site-VPN-Tunnel zum selben Virtual Private Gateway ergänzen",
       "Enhanced Networking auf den Instanzen in der VPC aktivieren",
       "Den Replikationsverkehr über ein NAT-Gateway leiten",
       "AWS Direct Connect bereitstellen und das VPN optional als verschlüsselten Ersatzpfad behalten"],
      "Direct Connect ist eine dedizierte private Netzwerkverbindung zwischen Kundenstandort und AWS und liefert genau die gleichmäßige Bandbreite und Latenz, die eine jitterempfindliche Massenübertragung braucht; das VPN als Rückfallebene zu behalten, ist der übliche ausfallsichere Hybridentwurf. Ein zweiter VPN-Tunnel läuft weiterhin über das öffentliche Internet und erbt dieselben Schwankungen. Enhanced Networking betrifft die Paketverarbeitung in der Instanz, nicht den Weitverkehrsweg. Ein NAT-Gateway dient ausgehendem Verkehr aus privaten Subnetzen und hat mit eingehender Replikation nichts zu tun."),
  ja=("ハイブリッドアプリケーションが、オンプレミスのデータセンターから VPC へ 1 日あたり数テラバイトをレプリケートしており、ジッターに敏感です。既存のパブリックインターネット経由 AWS Site-to-Site VPN では、スループットが安定しません。アーキテクトは何を推奨すべきですか。",
      ["同じ仮想プライベートゲートウェイに 2 本目の Site-to-Site VPN トンネルを追加する",
       "VPC 内のインスタンスで拡張ネットワーキングを有効にする",
       "レプリケーショントラフィックを NAT ゲートウェイ経由にする",
       "AWS Direct Connect をプロビジョニングし、必要に応じて VPN を暗号化されたバックアップ経路として残す"],
      "Direct Connect は顧客拠点と AWS を結ぶ専用のプライベートネットワーク接続であり、ジッターに敏感な大量転送に必要な安定した帯域とレイテンシーをもたらします。VPN をバックアップとして残す構成は、標準的な耐障害性のあるハイブリッド設計です。2 本目の VPN トンネルも結局パブリックインターネットを通るため、同じ変動をそのまま受け継ぎます。拡張ネットワーキングはインスタンス内部のパケット処理性能に関するもので、広域経路には影響しません。NAT ゲートウェイはプライベートサブネットからの送信トラフィック用であり、オンプレミスからの受信レプリケーションとは無関係です。"),
  zh=("某混合架构应用每天从本地数据中心向 VPC 复制数 TB 数据，并且对抖动敏感。现有的经公共互联网的 AWS Site-to-Site VPN 吞吐不稳定。架构师应推荐什么？",
      ["向同一个虚拟专用网关再增加一条 Site-to-Site VPN 隧道",
       "为 VPC 中的实例启用增强联网",
       "把复制流量改经 NAT 网关",
       "开通 AWS Direct Connect，并可选择保留 VPN 作为加密的备份链路"],
      "Direct Connect 是客户场所与 AWS 之间的专用私有网络连接，正好提供抖动敏感的大批量传输所需的稳定带宽与延迟；保留 VPN 作为备份是标准的高可用混合架构做法。再加一条 VPN 隧道仍然走公共互联网，继承同样的波动。增强联网影响的是实例内部的报文性能，与广域链路无关。NAT 网关服务于私有子网的出站流量，与来自本地的入站复制无关。"))

Q("aws-saa-performance-09", "high_performing_architectures",
  "Domain 3, Task Statement 3.1 (Determine high-performing and/or scalable storage solutions)",
  False, False, MC, ["b", "c"],
  "docs.aws.amazon.com/AmazonS3/latest/userguide/transfer-acceleration.html and docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html",
  en=("Field offices on four continents upload 20 GB video files to a single S3 bucket in eu-central-1. Uploads are slow and sometimes fail near the end. Which TWO changes improve throughput and reliability?",
      ["Change the bucket's storage class to S3 One Zone-IA",
       "Enable S3 Transfer Acceleration on the bucket and have clients use the accelerated endpoint",
       "Use multipart upload so that parts are transferred in parallel and only failed parts are retried",
       "Enable S3 Versioning on the bucket",
       "Batch all uploads into a single nightly window"],
      "Transfer Acceleration routes uploads to the nearest CloudFront edge location and then over the AWS network to the bucket's Region, which is what long-haul uploads need. Multipart upload splits the object into independently transferred parts, so bandwidth is used in parallel and a failure late in the transfer costs one part rather than the whole file; it is also mandatory here, because a single PUT is limited to 5 GB. Storage class and versioning affect how objects are stored and retained, not how fast they arrive, and a nightly window makes no individual upload any faster."),
  de=("Außenstellen auf vier Kontinenten laden 20-GB-Videodateien in einen einzigen S3-Bucket in eu-central-1. Die Uploads sind langsam und scheitern manchmal kurz vor dem Ende. Welche ZWEI Änderungen verbessern Durchsatz und Zuverlässigkeit?",
      ["Die Speicherklasse des Buckets auf S3 One Zone-IA ändern",
       "S3 Transfer Acceleration für den Bucket aktivieren und die Clients den beschleunigten Endpunkt verwenden lassen",
       "Multipart-Upload verwenden, damit Teile parallel übertragen und nur fehlgeschlagene Teile wiederholt werden",
       "S3-Versionierung für den Bucket aktivieren",
       "Alle Uploads in ein einziges nächtliches Zeitfenster bündeln"],
      "Transfer Acceleration leitet Uploads an den nächstgelegenen CloudFront-Edge-Standort und von dort über das AWS-Netz in die Region des Buckets - genau das, was Uploads über große Entfernungen brauchen. Multipart-Upload zerlegt das Objekt in unabhängig übertragene Teile, nutzt die Bandbreite parallel und macht einen späten Fehler zum Verlust eines Teils statt der ganzen Datei; hier ist er ohnehin zwingend, weil ein einzelnes PUT auf 5 GB begrenzt ist. Speicherklasse und Versionierung betreffen die Ablage und Aufbewahrung, nicht die Übertragungsgeschwindigkeit, und ein Nachtfenster macht keinen einzelnen Upload schneller."),
  ja=("4 大陸の拠点から 20 GB の動画ファイルを、eu-central-1 にある 1 つの S3 バケットへアップロードしています。アップロードが遅く、終盤で失敗することもあります。スループットと信頼性を高める変更はどの 2 つですか。",
      ["バケットのストレージクラスを S3 One Zone-IA に変更する",
       "バケットで S3 Transfer Acceleration を有効にし、クライアントに高速化エンドポイントを使わせる",
       "マルチパートアップロードを使い、パートを並列転送して失敗したパートだけを再試行する",
       "バケットで S3 バージョニングを有効にする",
       "すべてのアップロードを夜間の 1 つの時間帯にまとめる"],
      "Transfer Acceleration はアップロードを最寄りの CloudFront エッジロケーションへ導き、そこから AWS ネットワーク経由でバケットのリージョンへ転送します。長距離アップロードに必要なのはまさにこれです。マルチパートアップロードはオブジェクトを独立して転送されるパートに分割するため、帯域を並列に使え、転送終盤の失敗も 1 パート分の損失で済みます。さらに単一 PUT は 5 GB までなので、ここでは必須でもあります。ストレージクラスとバージョニングは保存と保持に関わるもので、到着速度は変えません。夜間にまとめても個々のアップロードは速くなりません。"),
  zh=("四大洲的分支机构向 eu-central-1 的同一个 S3 存储桶上传 20 GB 的视频文件。上传缓慢，有时在接近完成时失败。哪两项变更能提升吞吐与可靠性？",
      ["把存储桶的存储类别改为 S3 One Zone-IA",
       "为该存储桶启用 S3 传输加速，并让客户端使用加速终端节点",
       "使用分段上传，使各分段并行传输，且只重试失败的分段",
       "为该存储桶启用 S3 版本控制",
       "把所有上传集中到每晚的一个时间窗口"],
      "传输加速会把上传导向最近的 CloudFront 边缘站点，再经 AWS 网络送到存储桶所在区域，这正是跨洲上传所需要的。分段上传把对象拆成可独立传输的分段，从而并行利用带宽，并使传输后期的失败只损失一个分段而不是整个文件；而且在这里它本来就是必需的，因为单次 PUT 上限为 5 GB。存储类别和版本控制影响的是对象如何存放与保留，而不是传输速度；把上传集中到夜间窗口也不会让任何单次上传变快。"))

# ==========================================================================
# Domain 4 - Design Cost-Optimized Architectures (20% of scored) - 7 Q
# ==========================================================================

Q("aws-saa-cost-01", "cost_optimized_architectures",
  "Domain 4, Task Statement 4.1 (Design cost-optimized storage solutions)",
  False, False, SC, ["c"],
  "docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html and docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-transition-general-considerations.html",
  en=("Audit logs are queried constantly for their first 30 days and then only a few times a year, but whenever they are needed they must come back in milliseconds. They must be retained for seven years. Which S3 lifecycle design is the most cost-effective?",
      ["Keep everything in S3 Standard for the full seven years",
       "Transition to S3 Glacier Deep Archive at 30 days and expire the objects at seven years",
       "Transition to S3 Standard-IA at 30 days, then to S3 Glacier Instant Retrieval at 90 days, and expire the objects at seven years",
       "Transition to S3 One Zone-IA after one day and expire the objects at seven years"],
      "S3 Glacier Instant Retrieval is the archive class that still returns objects in milliseconds, so it is the only archive tier that satisfies the retrieval requirement, and its 90-day minimum storage duration is why the objects should spend the intervening period in Standard-IA (30-day minimum) rather than moving straight there. Deep Archive retrieval takes hours and breaks the requirement outright. One Zone-IA keeps a single copy in one Availability Zone, which is the wrong durability posture for seven-year audit records, and transitioning after one day is wasteful in any case because that class carries a 30-day minimum storage duration of its own."),
  de=("Prüfprotokolle werden in den ersten 30 Tagen ständig abgefragt und danach nur noch wenige Male pro Jahr - doch wenn sie gebraucht werden, müssen sie in Millisekunden verfügbar sein. Sie sind sieben Jahre aufzubewahren. Welcher S3-Lebenszyklusentwurf ist am wirtschaftlichsten?",
      ["Alles sieben Jahre lang in S3 Standard belassen",
       "Nach 30 Tagen nach S3 Glacier Deep Archive überführen und nach sieben Jahren ablaufen lassen",
       "Nach 30 Tagen nach S3 Standard-IA, nach 90 Tagen nach S3 Glacier Instant Retrieval überführen und nach sieben Jahren ablaufen lassen",
       "Nach einem Tag nach S3 One Zone-IA überführen und nach sieben Jahren ablaufen lassen"],
      "S3 Glacier Instant Retrieval ist die Archivklasse, die Objekte weiterhin in Millisekunden liefert, und damit die einzige Archivstufe, die die Abrufanforderung erfüllt. Ihre Mindestspeicherdauer von 90 Tagen ist der Grund, die Objekte zunächst in Standard-IA (30 Tage Mindestdauer) zu halten, statt direkt dorthin zu wechseln. Der Abruf aus Deep Archive dauert Stunden und verletzt die Anforderung unmittelbar. One Zone-IA hält nur eine Kopie in einer einzigen Availability Zone - die falsche Haltbarkeitsstufe für siebenjährige Prüfunterlagen -, und ein Wechsel nach einem Tag ist ohnehin verschwenderisch, weil diese Klasse selbst eine Mindestspeicherdauer von 30 Tagen hat."),
  ja=("監査ログは最初の 30 日間は絶えず参照され、その後は年に数回しか使われませんが、必要になったときはミリ秒で取り出せなければなりません。保持期間は 7 年です。最も費用対効果の高い S3 ライフサイクル設計はどれですか。",
      ["7 年間ずっと S3 Standard に置いたままにする",
       "30 日後に S3 Glacier Deep Archive へ移行し、7 年で失効させる",
       "30 日後に S3 Standard-IA、90 日後に S3 Glacier Instant Retrieval へ移行し、7 年で失効させる",
       "1 日後に S3 One Zone-IA へ移行し、7 年で失効させる"],
      "S3 Glacier Instant Retrieval はミリ秒で取り出せる唯一のアーカイブクラスであり、取り出し要件を満たすのはこれだけです。その最低保存期間が 90 日であるため、直接移行せず、その間は最低 30 日の Standard-IA に置くのが正解です。Deep Archive は取り出しに数時間かかり、要件を真っ向から破ります。One Zone-IA は単一アベイラビリティーゾーンに 1 コピーしか置かず、7 年保管の監査記録には不適切な耐久性です。さらに、このクラス自体が 30 日の最低保存期間を持つため、1 日で移行しても無駄になります。"),
  zh=("审计日志在最初 30 天内被频繁查询，之后每年只会用到几次，但一旦需要就必须在毫秒内返回。保留期为七年。哪种 S3 生命周期设计最具成本效益？",
      ["七年内始终保存在 S3 Standard 中",
       "30 天后转换到 S3 Glacier Deep Archive，七年后过期删除",
       "30 天后转换到 S3 Standard-IA，90 天后再转换到 S3 Glacier Instant Retrieval，七年后过期删除",
       "1 天后转换到 S3 One Zone-IA，七年后过期删除"],
      "S3 Glacier Instant Retrieval 是仍能在毫秒内返回对象的归档类别，因此是唯一满足取回要求的归档层；它有 90 天的最短存储时长，这正是应先把对象放在 Standard-IA（最短 30 天）过渡、而不是直接转入的原因。Deep Archive 的取回需要数小时，直接违反要求。One Zone-IA 只在单个可用区保留一份副本，对七年期审计记录而言持久性定位错误；而且该类别本身就有 30 天的最短存储时长，1 天就转换无论如何都是浪费。"))

Q("aws-saa-cost-02", "cost_optimized_architectures",
  "Domain 4, Task Statement 4.1 (Design cost-optimized storage solutions)",
  True, False, SC, ["a"],
  "docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html",
  en=("A data-science bucket holds objects whose access pattern is unknown and changes unpredictably. The team wants automatic cost optimisation with no retrieval charges and without writing and maintaining lifecycle rules. Which storage class should be used?",
      ["S3 Intelligent-Tiering",
       "S3 Standard-IA",
       "S3 One Zone-IA",
       "S3 Glacier Flexible Retrieval"],
      "Intelligent-Tiering moves each object between access tiers based on observed access, has no retrieval fees and no minimum storage duration, and charges a small per-object monitoring and automation fee instead. That combination is exactly what an unknown, changing access pattern needs. Standard-IA and One Zone-IA both carry per-GB retrieval fees and a 30-day minimum, so unpredictable access can end up costing more than S3 Standard would have. Glacier Flexible Retrieval takes minutes to hours to retrieve and has a 90-day minimum."),
  de=("Ein Data-Science-Bucket enthält Objekte, deren Zugriffsmuster unbekannt ist und sich unvorhersehbar ändert. Das Team möchte automatische Kostenoptimierung ohne Abrufgebühren und ohne selbst Lebenszyklusregeln zu pflegen. Welche Speicherklasse ist zu wählen?",
      ["S3 Intelligent-Tiering",
       "S3 Standard-IA",
       "S3 One Zone-IA",
       "S3 Glacier Flexible Retrieval"],
      "Intelligent-Tiering verschiebt jedes Objekt anhand des beobachteten Zugriffs zwischen Zugriffsstufen, kennt keine Abrufgebühren und keine Mindestspeicherdauer und berechnet stattdessen eine kleine Überwachungs- und Automatisierungsgebühr je Objekt. Genau diese Kombination braucht ein unbekanntes, wechselndes Zugriffsmuster. Standard-IA und One Zone-IA erheben beide Abrufgebühren je GB und eine Mindestdauer von 30 Tagen, sodass unvorhersehbare Zugriffe teurer werden können als S3 Standard. Glacier Flexible Retrieval braucht Minuten bis Stunden und hat 90 Tage Mindestdauer."),
  ja=("データサイエンス用のバケットに、アクセスパターンが不明で予測不能に変化するオブジェクトが入っています。チームは、取り出し料金がなく、ライフサイクルルールを自分で書いて維持することもなく、自動的にコスト最適化したいと考えています。どのストレージクラスを使うべきですか。",
      ["S3 Intelligent-Tiering",
       "S3 Standard-IA",
       "S3 One Zone-IA",
       "S3 Glacier Flexible Retrieval"],
      "Intelligent-Tiering は観測されたアクセス状況に基づいて各オブジェクトをアクセス階層間で移動させ、取り出し料金も最低保存期間もなく、代わりにオブジェクト単位の小額な監視・自動化料金がかかります。不明で変化するアクセスパターンに必要なのはまさにこの組み合わせです。Standard-IA と One Zone-IA はいずれも GB 単位の取り出し料金と 30 日の最低期間があり、予測不能なアクセスでは S3 Standard より高くつくことがあります。Glacier Flexible Retrieval は取り出しに数分から数時間かかり、最低 90 日です。"),
  zh=("某数据科学存储桶中的对象访问模式未知且不可预测地变化。团队希望在无取回费用、也不必自行编写和维护生命周期规则的情况下自动优化成本。应使用哪种存储类别？",
      ["S3 Intelligent-Tiering",
       "S3 Standard-IA",
       "S3 One Zone-IA",
       "S3 Glacier Flexible Retrieval"],
      "Intelligent-Tiering 会根据观测到的访问情况在各访问层之间移动对象，没有取回费用，也没有最短存储时长，取而代之的是每个对象少量的监控与自动化费用。这一组合正是未知且不断变化的访问模式所需要的。Standard-IA 和 One Zone-IA 都收取按 GB 的取回费并有 30 天最低期限，因此在访问不可预测时反而可能比 S3 Standard 更贵。Glacier Flexible Retrieval 取回需要数分钟到数小时，且最低 90 天。"))

Q("aws-saa-cost-03", "cost_optimized_architectures",
  "Domain 4, Task Statement 4.2 (Design cost-optimized compute solutions)",
  False, False, SC, ["d"],
  "docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html",
  en=("A company will run a steady baseline of compute for the next three years but expects to change instance families and even Regions as its workloads evolve, and it also runs AWS Fargate tasks. It wants the largest discount compatible with that flexibility. What should it commit to?",
      ["Standard Reserved Instances for a specific instance type in a specific Availability Zone",
       "On-Demand Capacity Reservations for the baseline capacity",
       "Spot Instances with a maximum price set equal to the On-Demand price",
       "A Compute Savings Plan with a committed hourly spend"],
      "A Compute Savings Plan applies an hourly spend commitment automatically across instance family, size, Region, operating system and tenancy, and also covers Fargate and Lambda usage - exactly the flexibility described. Standard Reserved Instances offer a comparable discount but lock in the very attributes the company says will change, and a zonal RI additionally fixes the Availability Zone. On-Demand Capacity Reservations reserve capacity but provide no discount by themselves. Spot cannot underpin a steady baseline because instances are reclaimed with two minutes' notice."),
  de=("Ein Unternehmen wird die nächsten drei Jahre eine gleichbleibende Grundlast an Rechenleistung betreiben, erwartet aber Wechsel bei Instanzfamilien und sogar Regionen und betreibt außerdem AWS-Fargate-Aufgaben. Es möchte den größten Rabatt, der mit dieser Flexibilität vereinbar ist. Worauf sollte es sich festlegen?",
      ["Standard Reserved Instances für einen bestimmten Instanztyp in einer bestimmten Availability Zone",
       "On-Demand Capacity Reservations für die Grundlast",
       "Spot-Instanzen mit einem Höchstpreis in Höhe des On-Demand-Preises",
       "Einen Compute Savings Plan mit zugesagter Stundenausgabe"],
      "Ein Compute Savings Plan wendet eine stündliche Ausgabenzusage automatisch über Instanzfamilie, -größe, Region, Betriebssystem und Mandantenform hinweg an und deckt zusätzlich Fargate- und Lambda-Nutzung ab - genau die beschriebene Flexibilität. Standard Reserved Instances bieten einen vergleichbaren Rabatt, legen aber genau die Merkmale fest, die sich laut Unternehmen ändern werden; eine zonale RI fixiert zusätzlich die Availability Zone. On-Demand Capacity Reservations sichern Kapazität, gewähren für sich genommen aber keinen Rabatt. Spot trägt keine gleichbleibende Grundlast, weil Instanzen mit zwei Minuten Vorlauf zurückgefordert werden."),
  ja=("ある企業は今後 3 年間、一定のベースライン分のコンピューティングを稼働させますが、ワークロードの変化に伴いインスタンスファミリーやリージョンを変更する見込みで、AWS Fargate のタスクも実行しています。この柔軟性と両立する最大の割引を求めています。何にコミットすべきですか。",
      ["特定アベイラビリティーゾーンの特定インスタンスタイプに対するスタンダードリザーブドインスタンス",
       "ベースライン容量に対するオンデマンドキャパシティ予約",
       "オンデマンド価格と同額の上限価格を設定したスポットインスタンス",
       "時間あたり支出をコミットする Compute Savings Plans"],
      "Compute Savings Plans は、時間あたりの支出コミットメントをインスタンスファミリー、サイズ、リージョン、OS、テナンシーを越えて自動的に適用し、さらに Fargate と Lambda の利用にも適用されます。まさに求められている柔軟性です。スタンダードリザーブドインスタンスは同程度の割引を提供しますが、変更が見込まれる属性そのものを固定してしまい、ゾーン指定の RI ではアベイラビリティーゾーンまで固定されます。オンデマンドキャパシティ予約は容量を確保しますが、それ自体に割引はありません。スポットは 2 分前の通知で回収されるため、一定のベースラインを支えることはできません。"),
  zh=("某公司未来三年将运行稳定的基线计算量，但预计随着工作负载演进会更换实例系列甚至区域，同时还运行 AWS Fargate 任务。它希望获得与这种灵活性相容的最大折扣。应当承诺哪种方案？",
      ["针对特定可用区中特定实例类型的标准预留实例",
       "针对基线容量的按需容量预留",
       "把最高价设为按需价格的 Spot 实例",
       "承诺每小时支出的 Compute Savings Plan"],
      "Compute Savings Plan 会把每小时支出承诺自动应用于不同实例系列、规格、区域、操作系统和租用模式，并且同样覆盖 Fargate 和 Lambda 用量——正是题中所述的灵活性。标准预留实例折扣相当，但恰好锁定了公司说会变化的那些属性，可用区级 RI 还会固定可用区。按需容量预留只保留容量，本身不提供折扣。Spot 无法支撑稳定基线，因为实例会在两分钟通知后被回收。"))

Q("aws-saa-cost-04", "cost_optimized_architectures",
  "Domain 4, Task Statement 4.2 (Design cost-optimized compute solutions)",
  True, False, SC, ["b"],
  "docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances.html",
  en=("A nightly media-transcoding job splits its work into thousands of independent tasks. Any task that is interrupted can simply be run again, and the job has a wide completion window. Which EC2 purchasing option minimises cost?",
      ["Dedicated Hosts",
       "Spot Instances, with the job written to handle the two-minute interruption notice",
       "On-Demand Instances in an Auto Scaling group",
       "All Upfront Standard Reserved Instances"],
      "Interruption-tolerant, stateless, time-flexible batch work is the canonical Spot use case and carries the steepest discount off On-Demand pricing; EC2 gives a two-minute interruption notice that a well-written job uses to checkpoint or simply abandon the task for a retry. Dedicated Hosts are the most expensive option and exist for licensing and physical-isolation requirements. On-Demand is the undiscounted baseline. Reserved Instances suit capacity that runs steadily around the clock, not a burst for part of each night."),
  de=("Ein nächtlicher Medien-Transkodierungsauftrag zerlegt seine Arbeit in Tausende unabhängiger Aufgaben. Jede unterbrochene Aufgabe kann einfach erneut ausgeführt werden, und der Auftrag hat ein weites Zeitfenster. Welche EC2-Kaufoption minimiert die Kosten?",
      ["Dedicated Hosts",
       "Spot-Instanzen, wobei der Auftrag den Zwei-Minuten-Unterbrechungshinweis verarbeitet",
       "On-Demand-Instanzen in einer Auto-Scaling-Gruppe",
       "Standard Reserved Instances mit vollständiger Vorauszahlung"],
      "Unterbrechungstolerante, zustandslose, zeitlich flexible Stapelverarbeitung ist der klassische Spot-Anwendungsfall und bietet den größten Rabatt auf den On-Demand-Preis; EC2 gibt einen Zwei-Minuten-Hinweis, den ein gut geschriebener Auftrag nutzt, um einen Prüfpunkt zu setzen oder die Aufgabe schlicht zur Wiederholung fallen zu lassen. Dedicated Hosts sind die teuerste Option und existieren für Lizenz- und Isolationsanforderungen. On-Demand ist der Listenpreis. Reserved Instances passen zu Kapazität, die rund um die Uhr gleichmäßig läuft, nicht zu einem Ausbruch in einem Teil jeder Nacht."),
  ja=("夜間のメディアトランスコードジョブは、作業を数千の独立したタスクに分割します。中断されたタスクは単に再実行すればよく、完了までの時間的余裕も広く取られています。コストを最小化する EC2 購入オプションはどれですか。",
      ["Dedicated Hosts",
       "2 分前の中断通知を処理できるように書かれたジョブで利用するスポットインスタンス",
       "Auto Scaling グループ内のオンデマンドインスタンス",
       "全額前払いのスタンダードリザーブドインスタンス"],
      "中断に強く、ステートレスで、時間的余裕のあるバッチ処理はスポットの典型的なユースケースであり、オンデマンド価格に対する割引幅が最も大きくなります。EC2 は 2 分前に中断通知を出し、適切に書かれたジョブはそれを使ってチェックポイントを取るか、単にタスクを破棄して再試行に回します。Dedicated Hosts は最も高価で、ライセンスや物理的分離の要件のために存在します。オンデマンドは割引のない基準価格です。リザーブドインスタンスは 24 時間安定して稼働する容量に向いており、毎晩一部の時間帯だけ発生するバーストには向きません。"),
  zh=("某夜间媒体转码作业把工作拆分为数千个相互独立的任务。任何被中断的任务只需重新运行即可，且作业的完成时间窗口很宽。哪种 EC2 购买选项成本最低？",
      ["专用主机（Dedicated Hosts）",
       "Spot 实例，并让作业处理两分钟中断通知",
       "Auto Scaling 组中的按需实例",
       "全额预付的标准预留实例"],
      "可容忍中断、无状态、时间灵活的批处理正是 Spot 的典型场景，相对按需价格折扣最大；EC2 会提前两分钟发出中断通知，编写良好的作业可据此做检查点或直接放弃该任务等待重试。专用主机是最贵的选项，主要用于许可与物理隔离需求。按需是无折扣的基准价格。预留实例适合全天候稳定运行的容量，而不是每晚只持续一段时间的突发负载。"))

Q("aws-saa-cost-05", "cost_optimized_architectures",
  "Domain 4, Task Statement 4.4 (Design cost-optimized network architectures)",
  False, False, SC, ["a"],
  "docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html and docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-basics.html",
  en=("Instances in private subnets pull several terabytes per month from Amazon S3 in the same Region, and all of that traffic currently flows through NAT gateways. Which change reduces cost the most, and why?",
      ["Add a gateway VPC endpoint for Amazon S3, because the endpoint carries no additional charge and its route takes precedence, so the traffic no longer touches the NAT gateways",
       "Add an interface VPC endpoint for Amazon S3, because interface endpoints are free of charge",
       "Move the instances into public subnets with public IP addresses, because internet gateways charge per GB",
       "Enable S3 Transfer Acceleration, because it lowers the per-GB data charge"],
      "NAT gateways bill both per hour and per GB processed, so multi-terabyte S3 traffic is expensive purely in data-processing fees. AWS states there is no additional charge for gateway endpoints, and because the endpoint route is a more specific prefix-list match than the 0.0.0.0/0 route, S3 traffic leaves the NAT path automatically once the route is added. Interface endpoints are not free: they bill per endpoint-hour and per GB. Internet gateways are not charged per GB, so option c is wrong on its own reasoning as well as on security grounds. Transfer Acceleration adds a per-GB charge rather than removing one."),
  de=("Instanzen in privaten Subnetzen holen monatlich mehrere Terabyte aus Amazon S3 in derselben Region, und dieser gesamte Verkehr läuft derzeit über NAT-Gateways. Welche Änderung senkt die Kosten am stärksten, und warum?",
      ["Einen Gateway-VPC-Endpunkt für Amazon S3 ergänzen, weil für den Endpunkt keine zusätzliche Gebühr anfällt und seine Route Vorrang hat, sodass der Verkehr die NAT-Gateways nicht mehr berührt",
       "Einen Interface-VPC-Endpunkt für Amazon S3 ergänzen, weil Interface-Endpunkte kostenlos sind",
       "Die Instanzen in öffentliche Subnetze mit öffentlichen IP-Adressen verschieben, weil Internet-Gateways pro GB abrechnen",
       "S3 Transfer Acceleration aktivieren, weil es die Datengebühr je GB senkt"],
      "NAT-Gateways werden sowohl je Stunde als auch je verarbeitetem GB abgerechnet; mehrere Terabyte S3-Verkehr sind allein an Datenverarbeitungsgebühren teuer. Laut AWS fallen für Gateway-Endpunkte keine zusätzlichen Gebühren an, und da die Endpunktroute ein spezifischerer Präfixlisten-Treffer ist als die 0.0.0.0/0-Route, verlässt der S3-Verkehr den NAT-Pfad automatisch, sobald die Route eingetragen ist. Interface-Endpunkte sind nicht kostenlos: Sie werden je Endpunktstunde und je GB berechnet. Internet-Gateways rechnen nicht je GB ab, Antwort c ist also schon in ihrer eigenen Begründung falsch. Transfer Acceleration fügt eine Gebühr je GB hinzu, statt eine zu beseitigen."),
  ja=("プライベートサブネット内のインスタンスが、同一リージョンの Amazon S3 から月に数テラバイトを取得しており、その全トラフィックが現在 NAT ゲートウェイを経由しています。最もコストを下げる変更はどれで、その理由は何ですか。",
      ["Amazon S3 用のゲートウェイ VPC エンドポイントを追加する。エンドポイント自体に追加料金がなく、そのルートが優先されるため、トラフィックが NAT ゲートウェイを通らなくなるから",
       "Amazon S3 用のインターフェイス VPC エンドポイントを追加する。インターフェイスエンドポイントは無料だから",
       "インスタンスをパブリック IP 付きのパブリックサブネットに移す。インターネットゲートウェイは GB 単位で課金されるから",
       "S3 Transfer Acceleration を有効にする。GB 単位のデータ料金が下がるから"],
      "NAT ゲートウェイは時間単位と処理 GB 単位の両方で課金されるため、数テラバイトの S3 トラフィックはデータ処理料金だけでも高額になります。AWS はゲートウェイエンドポイントに追加料金はないと明記しており、エンドポイントのルートは 0.0.0.0/0 より具体的なプレフィックスリスト一致となるため、ルートを追加した時点で S3 トラフィックは自動的に NAT 経路から外れます。インターフェイスエンドポイントは無料ではなく、エンドポイント時間単位と GB 単位で課金されます。インターネットゲートウェイは GB 単位で課金されないため、選択肢 c は理由付け自体が誤りです。Transfer Acceleration は GB 単位の料金を減らすどころか追加します。"),
  zh=("私有子网中的实例每月从同一区域的 Amazon S3 拉取数 TB 数据，目前这些流量全部经由 NAT 网关。哪项变更能最大幅度降低成本，为什么？",
      ["为 Amazon S3 添加网关 VPC 终端节点：该终端节点不收取额外费用，且其路由优先级更高，因此流量不再经过 NAT 网关",
       "为 Amazon S3 添加接口 VPC 终端节点：接口终端节点是免费的",
       "把实例迁到带公网 IP 的公有子网：因为互联网网关按 GB 收费",
       "启用 S3 传输加速：因为它会降低按 GB 的数据费用"],
      "NAT 网关同时按小时和按处理的 GB 计费，因此数 TB 的 S3 流量仅数据处理费就非常昂贵。AWS 明确说明网关终端节点不收取额外费用，而且由于终端节点路由是比 0.0.0.0/0 更具体的前缀列表匹配，一旦添加路由，S3 流量就会自动脱离 NAT 路径。接口终端节点并不免费：它按终端节点小时和 GB 计费。互联网网关并不按 GB 计费，因此选项 c 的理由本身就是错的。传输加速是增加而不是减少按 GB 的费用。"))

Q("aws-saa-cost-06", "cost_optimized_architectures",
  "Domain 4, Task Statement 4.1 (Design cost-optimized storage solutions)",
  True, False, MC, ["a", "d"],
  "docs.aws.amazon.com/AmazonS3/latest/userguide/mpu-abort-incomplete-mpu-lifecycle-config.html and docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html",
  en=("A cost review of an S3 bucket finds a large amount of billed storage that nobody can account for in the object listing, plus a set of easily regenerated thumbnail images kept in S3 Standard. Which TWO changes reduce cost without putting production data at risk?",
      ["Add a lifecycle rule that aborts incomplete multipart uploads after seven days",
       "Suspend S3 Versioning on the bucket, which deletes all existing noncurrent versions",
       "Transition every object in the bucket to S3 Glacier Deep Archive",
       "Store the regenerable thumbnails in S3 One Zone-IA",
       "Turn off default encryption to avoid AWS KMS request charges"],
      "Parts of an incomplete multipart upload are billed as storage but do not appear as objects in a normal listing, which is the classic explanation for unaccounted-for storage; the AbortIncompleteMultipartUpload lifecycle action is the standard remedy. One Zone-IA stores a single copy in one Availability Zone at a lower price and is appropriate precisely for reproducible data. Option b is wrong twice over: suspending versioning does not delete existing noncurrent versions (a lifecycle expiration rule does), and it removes a data-protection control. Deep Archive would break any millisecond access requirement across the whole bucket. Turning off encryption trades a security control for a trivial saving."),
  de=("Eine Kostenprüfung eines S3-Buckets findet eine große Menge berechneten Speichers, die sich in der Objektliste nicht wiederfindet, sowie leicht neu erzeugbare Vorschaubilder in S3 Standard. Welche ZWEI Änderungen senken die Kosten, ohne Produktivdaten zu gefährden?",
      ["Eine Lebenszyklusregel ergänzen, die unvollständige Multipart-Uploads nach sieben Tagen abbricht",
       "Die S3-Versionierung des Buckets aussetzen, wodurch alle vorhandenen älteren Versionen gelöscht werden",
       "Alle Objekte des Buckets nach S3 Glacier Deep Archive überführen",
       "Die neu erzeugbaren Vorschaubilder in S3 One Zone-IA ablegen",
       "Die Standardverschlüsselung abschalten, um AWS-KMS-Anfragegebühren zu vermeiden"],
      "Teile eines unvollständigen Multipart-Uploads werden als Speicher berechnet, erscheinen in einer normalen Auflistung aber nicht als Objekte - die klassische Erklärung für unerklärlichen Speicher; die Lebenszyklusaktion AbortIncompleteMultipartUpload ist das übliche Gegenmittel. One Zone-IA hält eine einzelne Kopie in einer Availability Zone zu geringerem Preis und passt genau zu reproduzierbaren Daten. Antwort b ist doppelt falsch: Das Aussetzen der Versionierung löscht vorhandene ältere Versionen nicht (das tut eine Ablaufregel), und es entfernt einen Datenschutzmechanismus. Deep Archive würde jede Millisekundenanforderung für den gesamten Bucket brechen. Die Verschlüsselung abzuschalten tauscht eine Sicherheitsmaßnahme gegen eine minimale Ersparnis."),
  ja=("S3 バケットのコスト見直しで、オブジェクト一覧では説明のつかない大量の課金対象ストレージと、S3 Standard に置かれた再生成が容易なサムネイル画像群が見つかりました。本番データを危険にさらさずにコストを下げる変更はどの 2 つですか。",
      ["未完了のマルチパートアップロードを 7 日後に中止するライフサイクルルールを追加する",
       "バケットの S3 バージョニングを停止する。これにより既存の非現行バージョンがすべて削除される",
       "バケット内のすべてのオブジェクトを S3 Glacier Deep Archive へ移行する",
       "再生成可能なサムネイルを S3 One Zone-IA に保存する",
       "AWS KMS のリクエスト料金を避けるためデフォルト暗号化を無効にする"],
      "未完了マルチパートアップロードのパートはストレージとして課金されますが、通常の一覧にはオブジェクトとして現れません。説明のつかないストレージの典型的な原因であり、AbortIncompleteMultipartUpload ライフサイクルアクションが標準的な対処です。One Zone-IA は単一アベイラビリティーゾーンに 1 コピーを低価格で保存するもので、再生成可能なデータにはまさに適しています。選択肢 b は二重に誤りです。バージョニングの停止は既存の非現行バージョンを削除せず(削除するのはライフサイクルの有効期限ルール)、しかもデータ保護の仕組みを外してしまいます。Deep Archive はバケット全体でミリ秒アクセス要件を壊します。暗号化の無効化はごくわずかな節約のためにセキュリティ統制を手放す行為です。"),
  zh=("对某 S3 存储桶的成本审查发现：有大量计费存储在对象列表中无从解释；同时还有一批容易重新生成的缩略图保存在 S3 Standard 中。哪两项变更能在不危及生产数据的前提下降低成本？",
      ["添加生命周期规则，在 7 天后中止未完成的分段上传",
       "暂停该存储桶的 S3 版本控制，这会删除所有现存的非当前版本",
       "把该存储桶中的所有对象转换到 S3 Glacier Deep Archive",
       "把可重新生成的缩略图存放到 S3 One Zone-IA",
       "关闭默认加密以避免 AWS KMS 请求费用"],
      "未完成分段上传的分段会按存储计费，但在常规列表中并不显示为对象，这正是“无从解释的存储”的典型成因；AbortIncompleteMultipartUpload 生命周期操作是标准解决办法。One Zone-IA 以更低价格在单个可用区保存一份副本，恰好适合可重新生成的数据。选项 b 有双重错误：暂停版本控制并不会删除现存的非当前版本（那需要生命周期过期规则），而且还移除了一项数据保护措施。Deep Archive 会让整个存储桶都无法满足毫秒级访问要求。关闭加密是用一项安全控制换取微不足道的节省。"))

Q("aws-saa-cost-07", "cost_optimized_architectures",
  "Domain 4, Task Statement 4.3 (Design cost-optimized database solutions)",
  False, False, SC, ["c"],
  "docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.html",
  en=("A development Amazon Aurora PostgreSQL cluster is busy for a few hours on weekdays and idle at night and at weekends. The team wants to stop paying for provisioned capacity that is not used, without rewriting the application. Which option fits?",
      ["Buy Standard Reserved Instances for the cluster",
       "Migrate the data to Amazon DynamoDB with on-demand capacity",
       "Convert the cluster to Amazon Aurora Serverless v2, which adjusts capacity in fine-grained increments as demand changes",
       "Run the database on an EC2 Spot Instance"],
      "Aurora Serverless v2 scales Aurora Capacity Units up and down in fine-grained increments in response to load, so an idle development cluster costs a small fraction of an equivalently sized provisioned one, and the PostgreSQL wire protocol and SQL surface are unchanged, so the application needs no rewrite. Reserved Instances commit to exactly the capacity the team has just said goes unused. Moving to DynamoDB is a different data model and a full application rewrite. Aurora is a managed service; you cannot run its instances on Spot."),
  de=("Ein Entwicklungscluster mit Amazon Aurora PostgreSQL ist werktags einige Stunden ausgelastet und nachts sowie am Wochenende im Leerlauf. Das Team möchte aufhören, für ungenutzte bereitgestellte Kapazität zu zahlen, ohne die Anwendung umzuschreiben. Welche Option passt?",
      ["Standard Reserved Instances für den Cluster kaufen",
       "Die Daten nach Amazon DynamoDB mit On-Demand-Kapazität migrieren",
       "Den Cluster auf Amazon Aurora Serverless v2 umstellen, das die Kapazität in feinen Schritten an die Nachfrage anpasst",
       "Die Datenbank auf einer EC2-Spot-Instanz betreiben"],
      "Aurora Serverless v2 skaliert Aurora Capacity Units in feinen Schritten mit der Last, sodass ein untätiger Entwicklungscluster nur einen Bruchteil eines gleich großen bereitgestellten Clusters kostet; das PostgreSQL-Protokoll und die SQL-Oberfläche bleiben unverändert, die Anwendung muss also nicht angefasst werden. Reserved Instances legen genau die Kapazität fest, die laut Team ungenutzt bleibt. Ein Wechsel zu DynamoDB bedeutet ein anderes Datenmodell und eine vollständige Umschreibung. Aurora ist ein verwalteter Dienst; seine Instanzen lassen sich nicht auf Spot betreiben."),
  ja=("開発用の Amazon Aurora PostgreSQL クラスターは、平日に数時間だけ負荷がかかり、夜間と週末はアイドル状態です。チームはアプリケーションを書き換えずに、使われていないプロビジョニング容量への支払いをやめたいと考えています。適切な選択肢はどれですか。",
      ["クラスター向けにスタンダードリザーブドインスタンスを購入する",
       "データをオンデマンドキャパシティの Amazon DynamoDB に移行する",
       "クラスターを Amazon Aurora Serverless v2 に変換する。需要に応じて細かい単位で容量が調整される",
       "データベースを EC2 スポットインスタンス上で稼働させる"],
      "Aurora Serverless v2 は負荷に応じて Aurora Capacity Unit を細かい単位で増減させるため、アイドル状態の開発クラスターは同規模のプロビジョニング済みクラスターのごく一部のコストで済みます。PostgreSQL のワイヤプロトコルと SQL の互換性はそのままなので、アプリケーションの書き換えも不要です。リザーブドインスタンスは、まさに使われていないと述べられた容量をコミットしてしまいます。DynamoDB への移行はデータモデルが異なり、アプリケーションの全面書き換えになります。Aurora はマネージドサービスであり、そのインスタンスをスポットで動かすことはできません。"),
  zh=("某开发用 Amazon Aurora PostgreSQL 集群在工作日只有几个小时繁忙，夜间和周末处于空闲状态。团队希望在不重写应用的前提下，停止为未被使用的预置容量付费。哪个选项合适？",
      ["为该集群购买标准预留实例",
       "将数据迁移到采用按需容量的 Amazon DynamoDB",
       "把集群转换为 Amazon Aurora Serverless v2，它会随需求以细粒度增量调整容量",
       "在 EC2 Spot 实例上运行该数据库"],
      "Aurora Serverless v2 会随负载以细粒度增量上下调整 Aurora 容量单位，因此空闲的开发集群成本只是同规模预置集群的一小部分；同时 PostgreSQL 的通信协议与 SQL 接口保持不变，应用无需重写。预留实例恰恰承诺了团队刚说未被使用的那部分容量。迁移到 DynamoDB 意味着完全不同的数据模型和彻底的应用重写。Aurora 是托管服务，其实例无法运行在 Spot 上。"))


# ==========================================================================
# Module metadata
# ==========================================================================

META = {
    "app": "Zettacard / aws-saa-lernmodul",
    "version": "0.1-draft",
    "generated": "2026-08-24",
    "generator": "authored:claude-opus/2026-08-24 (data/gen_aws_saa_draft.py)",
    "description": (
        "Original practice questions for the AWS Certified Solutions Architect - "
        "Associate certification, exam code SAA-C03. Unlike Zettacard's cka module, "
        "this one CAN honestly describe itself as format-faithful: AWS's own exam "
        "guide states that SAA-C03 consists of 65 questions (50 scored, 15 unscored) "
        "that are either multiple choice (one correct response, three distractors) or "
        "multiple response (two or more correct responses out of five or more options), "
        "sat in 130 minutes for 150 USD, scored 100-1,000 with a passing score of 720 "
        "on a compensatory model. There is NO hands-on or performance-based component "
        "anywhere in the SAA exam - which is why cka's standing disclaimer ('the real "
        "exam is 100% hands-on, this is a concept-check, not an exam simulator') does "
        "NOT apply here and must not be copied across. "
        "The four content domains and their weightings are taken from the same exam "
        "guide: Design Secure Architectures 30%, Design Resilient Architectures 26%, "
        "Design High-Performing Architectures 24%, Design Cost-Optimized Architectures "
        "20%. This 36-question pilot distributes questions across those four domains in "
        "approximately those proportions (11/9/9/7). "
        "WHAT THIS MODULE IS NOT: it is unofficial practice material, not affiliated "
        "with, sponsored by or endorsed by Amazon Web Services. AWS exam content is "
        "confidential under the AWS Certification Agreement and none of it is reproduced "
        "here: every scenario, option, distractor and explanation was authored from the "
        "public exam guide's task statements plus public AWS service documentation, and "
        "no commercial exam-prep vendor's question bank, 'dump' site, paid AWS training "
        "course or third-party book was consulted at any point (AGENTS.md constraint 1). "
        "Passing every question here is not a prediction of passing the real exam, whose "
        "question pool is not public and cannot be."
    ),
    "class": "ALL",
    "locales": LOCALES,
    "canonical_locale": "en",
    "locale_note": (
        "EN is canonical: AWS authors the exam and its documentation in English, and "
        "AWS service names are not translated in any locale here. The four-locale set "
        "en/de/ja/zh deliberately MIRRORS THE cka PRECEDENT of 2026-08-15 (the first "
        "module to depart from the repo's 12-locale rule and the first with EN as the "
        "source locale, both PO-approved for a first-of-its-kind technical-certification "
        "module). It is NOT a fresh exception being claimed on this module's own merits. "
        "If the PO would rather technical-certification modules carry the full 12 "
        "locales from day one, that decision applies equally to cka and to this module, "
        "and nothing in the schema here assumes four."
    ),
    "exam_format_note": (
        "Real exam, per AWS's own exam guide and certification page (retrieved "
        "2026-08-24): 65 questions total, of which 50 are scored and 15 are unscored "
        "and do not affect the score; question types are multiple choice and multiple "
        "response ONLY; 130 minutes; 150 USD; scaled score 100-1,000 with 720 to pass; "
        "compensatory scoring, so there is no per-domain pass requirement. AWS does not "
        "publish the ratio of multiple-response to multiple-choice questions, so this "
        "pilot's 5-of-36 (about 14%) multi-select share is an authoring choice, not a "
        "claim about the real exam, and is flagged as such rather than presented as a "
        "verified figure. This 36-question pilot is NOT a 65-question mock exam; a "
        "full-length timed mock is a later card, not this one."
    ),
    "topic_weighting_note": (
        "topic_code maps 1:1 onto the four content domains AWS publishes, so the "
        "distribution is checkable against the published weightings rather than being "
        "an internal taxonomy. Domain weights 30/26/24/20 against a 36-question pilot "
        "give 10.8/9.36/8.64/7.2 questions; the pilot ships 11/9/9/7, i.e. 30.6/25.0/"
        "25.0/19.4 percent, every domain within 1.0 percentage point of its published "
        "weight. The task statement each question was authored against is recorded in "
        "its legal_basis field, which also names the AWS documentation page the correct "
        "answer was verified against."
    ),
    "topic_labels": {code: DOMAINS[code]["label"] for code in DOMAINS},
    "domain_weights_percent": {code: DOMAINS[code]["weight"] for code in DOMAINS},
    "point_system": (
        "1 point for grundstoff (fundamentals) questions, 2 points for the applied "
        "scenario tier - same convention as the cka module. These are Zettacard's own "
        "practice weights and have nothing to do with AWS's scaled scoring, which is "
        "100-1,000 with a 720 pass mark and is not a percentage."
    ),
    "pass_rule_note": (
        "Do NOT present any percentage from this module as an AWS pass mark. AWS scores "
        "on a scaled 100-1,000 range where 720 passes; a scaled score is not a "
        "percentage of questions answered correctly and cannot be converted into one. "
        "Any in-app pass threshold for this module is a Zettacard practice threshold and "
        "must be labelled as such."
    ),
    "sources": {
        "tier_a_exam_structure": [
            "AWS Certified Solutions Architect - Associate (SAA-C03) Exam Guide, "
            "docs.aws.amazon.com/aws-certification/latest/solutions-architect-associate-03/"
            "solutions-architect-associate-03.html and the PDF at "
            "docs.aws.amazon.com/pdfs/aws-certification/latest/solutions-architect-associate-03/"
            "solutions-architect-associate-03.pdf - retrieved 2026-08-24. Source of the "
            "exam code, 50 scored + 15 unscored questions, 720/1,000 passing score, "
            "compensatory scoring, the four domains, their weightings and the fourteen "
            "task statements.",
            "AWS certification product page, "
            "aws.amazon.com/certification/certified-solutions-architect-associate/ - "
            "retrieved 2026-08-24. Source of '65 questions; either multiple choice or "
            "multiple response', 130 minutes, 150 USD.",
            "AWS Certification 'Coming Soon' page, aws.amazon.com/certification/coming-soon/ "
            "- retrieved 2026-08-24. Checked specifically to confirm SAA-C03 is still "
            "current: the only exam update listed is SysOps Administrator - Associate "
            "becoming CloudOps Engineer - Associate (SOA-C02 -> SOA-C03, last SOA-C02 day "
            "2025-09-29). No SAA-C04 or SAA update is announced by AWS.",
        ],
        "tier_a_service_behaviour": [
            "docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html - "
            "storage-class AZ counts, minimum storage durations (30/90/180 days), "
            "retrieval fees and retrieval times.",
            "docs.aws.amazon.com/AmazonS3/latest/userguide/replication-requirements.html - "
            "versioning required on both source and destination for live replication.",
            "docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html - gateway "
            "endpoints exist for S3 and DynamoDB only; no additional charge; longest-prefix "
            "precedence over a 0.0.0.0/0 route.",
            "docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-basics.html - a NAT "
            "gateway is created in a specific AZ and is redundant only within it; AWS "
            "recommends one per AZ with same-AZ routing.",
            "docs.aws.amazon.com/vpc/latest/userguide/infrastructure-security.html - the "
            "security group vs network ACL comparison (stateful/stateless, instance/subnet "
            "level, allow-only vs allow-and-deny, all-rules vs ordered evaluation).",
            "docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZSingleStandby.html "
            "- 'You can't use a standby replica to serve read traffic.'",
            "docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Replication.html - "
            "up to 15 Aurora Replicas, shared cluster volume, automatic promotion.",
            "docs.aws.amazon.com/ebs/latest/userguide/general-purpose.html - gp3 includes "
            "3,000 IOPS and 125 MiB/s at any size and does not use burst performance; gp2 "
            "baseline is 3 IOPS per GiB with bursting to 3,000.",
            "docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html - "
            "NLB is layer 4, supports one Elastic IP per enabled subnet, TCP/UDP/TLS.",
            "docs.aws.amazon.com/global-accelerator/latest/dg/what-is-global-accelerator.html "
            "- two static anycast IPv4 addresses (four for dual-stack) from the AWS edge "
            "network.",
            "Further pages named per question in the legal_basis field: IAM roles for EC2, "
            "IAM best practices, cross-account roles and external IDs, Organizations SCPs, "
            "AWS WAF, Shield Advanced, KMS concepts, S3 SSE-KMS, Secrets Manager rotation, "
            "CloudFront origin access control, ACM/ALB HTTPS listeners, SQS FIFO queues, "
            "SQS dead-letter queues, SNS fan-out, Auto Scaling on an SQS backlog, Route 53 "
            "failover routing, EFS, DynamoDB DAX, Lambda provisioned concurrency, Amazon "
            "Data Firehose, FSx for Lustre, Direct Connect, S3 Transfer Acceleration, S3 "
            "multipart upload, Savings Plans, Spot Instances, Aurora Serverless v2.",
        ],
        "licensing_and_trademark": [
            "AWS Site Terms, aws.amazon.com/terms/ - retrieved 2026-08-24. AWS Site "
            "content is AWS's property; the licence granted to visitors is limited to "
            "personal use and expressly excludes commercial use and derivative use. This "
            "is the reason nothing from AWS's documentation is reproduced here and every "
            "sentence in this file is independently authored: AWS documentation is a "
            "factual reference for this module, never an ingested corpus. Contrast cka, "
            "where the CNCF curriculum's CC-BY licence permitted ingestion with "
            "attribution.",
            "AWS Trademark Guidelines, aws.amazon.com/trademark-guidelines/ - retrieved "
            "2026-08-24. 'AWS does not object to fair use of its marks by third parties, "
            "so long as the use would not be confusing for customers' and 'AWS does not "
            "object to limited fair use of such materials for educational or non-profit "
            "purposes', but 'Fair use does not permit you to state or imply affiliation, "
            "sponsorship, or endorsement by AWS.'",
            "AWS Certification Agreement, aws.amazon.com/certification/certification-agreement/ "
            "- retrieved 2026-08-24. 'You agree that all Credential Assessment Materials "
            "are AWS Confidential Information'; candidates must not 'disclose or "
            "disseminate the content of any Certification Exam'. Recorded here because it "
            "is the reason this module must never ingest recalled or 'dumped' exam "
            "questions from any source.",
        ],
    },
    "not_used_as_sources": (
        "No commercial exam-prep vendor's question text, explanations, wording or "
        "structure; no 'dump', 'braindump' or recalled-question site; no paid AWS "
        "training course, Udemy course or third-party book; no AWS Skill Builder "
        "practice-exam content. Search results for this topic are dominated by such "
        "vendors and none was fetched. AGENTS.md constraint 1 bans third-party exam-prep "
        "companies' text outright, and unlike the StVO sign-icon carve-out there is no "
        "visual-accuracy exception that could apply to a question bank."
    ),
    "trademark_note": (
        "AWS, Amazon Web Services, and the AWS service names used in this module are "
        "trademarks of Amazon.com, Inc. or its affiliates, used nominatively to name the "
        "services the certification covers. Zettacard is not affiliated with, sponsored "
        "by, endorsed by or certified by AWS. Before any public launch, the module label "
        "and landing copy must be checked against AWS's trademark guidelines and against "
        "app/legal/marken.html / app/legal/quellen.html, and an AWS row added to the "
        "per-source table in quellen.html (body/source: Amazon Web Services, Inc.; "
        "licence: AWS Site Terms, no reuse licence, used as factual reference only; note: "
        "exam guide and public service documentation, no AWS text reproduced)."
    ),
    "related_modules": {
        "cka": (
            "The sibling technical-certification module and the precedent this one "
            "follows for locale scope (en/de/ja/zh, EN canonical). The two differ on one "
            "point that must NOT be copied across: cka disclaims itself as 'not an exam "
            "simulator' because the real CKA exam is 100% performance-based, while SAA-C03 "
            "is multiple choice / multiple response only and therefore has no such excuse. "
            "See docs/cka-lab-and-cloud-cert-hands-on-scoping-2026-08-23.md, which "
            "established this finding for the PO."
        ),
        "it_sicherheit": (
            "Overlaps only in vocabulary. it_sicherheit is a German workplace-compliance "
            "module on BSI/ISO-grounded information security; this module is vendor-"
            "specific cloud architecture. No question is shared or adapted in either "
            "direction."
        ),
        "nis2_dora": (
            "Deliberately NOT linked. The EU regulatory modules test legal obligations; "
            "SAA-C03 tests AWS service selection. Cloud-outsourcing overlap exists at the "
            "business level but there is no question-level relationship, and mixing them "
            "would mis-sell both."
        ),
    },
    "legal_review_status": (
        "NOT legally reviewed - AI-drafted DRAFT, 2026-08-24, and not reviewed by anyone. "
        "This is not law-based content, so no counsel-review track applies the way it does "
        "for the compliance modules; the discipline is kept per AGENTS.md constraint 4 all "
        "the same. Two things DO need human sign-off before this can ship, and neither is "
        "a legal review in the statutory sense: (1) a technical accuracy review of all 36 "
        "questions by someone who holds the certification or works with these services "
        "daily - every correct answer here was verified against AWS's own documentation "
        "on 2026-08-24, but that is self-verification by the drafting agent and AGENTS.md's "
        "working discipline says an agent's own claim that its work is right is not "
        "verification; (2) a trademark and positioning check on the module label and "
        "landing copy against AWS's trademark guidelines (see meta.trademark_note). Must "
        "not be shipped to learners before both."
    ),
    "renewal_months": 6,
    "renewal_basis": (
        "AWS revises certification exams on its own schedule and retires exam versions "
        "with a published last-day date; it also changes service behaviour, storage-class "
        "terms and pricing continuously. SAA-C03 was confirmed current on 2026-08-24 "
        "against AWS's own 'Coming Soon' page, which announced no SAA update."
    ),
    "renewal_note": (
        "Re-verification due no later than 2027-02-28, and earlier if AWS announces an SAA "
        "update. Two distinct checks, not one: (1) is the exam version still SAA-C03, and "
        "are the domain weightings, question counts and passing score unchanged? Read them "
        "from AWS's exam guide and Coming Soon page, never from this file. (2) has any "
        "asserted service behaviour changed? The volatile ones here are S3 storage-class "
        "minimum durations and retrieval characteristics, EBS gp3 defaults and maxima, "
        "Aurora replica limits, Aurora Serverless v2 capacity behaviour, Savings Plans "
        "coverage, and the 5 GB single-PUT limit. NOTE for the next agent: third-party "
        "sites were already publishing 'SAA-C04' guides on 2026-08-24 while AWS itself "
        "announced no such exam. Do not take a vendor blog's word for an exam version; "
        "check aws.amazon.com/certification/coming-soon/ and the exam guide's own URL slug."
    ),
    "draft_note": (
        "Not registered in data/build_modules.py, not in data/modules_manifest.json, "
        "app/ untouched (no app.js change, no locale files, no app/data/ output), no "
        "build step run, nothing staged or committed. The _DRAFT filename suffix keeps "
        "this file out of the live build path by construction, exactly as for "
        "bewachungsgewerbe_pilot_DRAFT.json and the other draft modules. First-round "
        "pilot: 36 questions, EN canonical + DE + JA + ZH. See "
        "docs/aws-saa-pre-review-dossier-2026-08-24.md for the sourcing analysis, the "
        "licensing analysis (which is materially different from cka's) and the open items "
        "the PO has to decide before this is wired in."
    ),
    "license": "CC BY-NC-SA 4.0",
    "license_url": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
    "license_note": (
        "CC BY-NC-SA 4.0, the repo default under LICENSE.md, and here the default is "
        "correct rather than merely convenient - checked, not assumed. AGENTS.md "
        "constraint 3 requires a module to declare its REAL licence when it ingests "
        "third-party material under different terms. This module ingests none. AWS's exam "
        "guide and service documentation carry no reuse licence at all: the AWS Site Terms "
        "grant only a limited personal-use licence and expressly exclude commercial and "
        "derivative use, so they could not have been ingested even if we had wanted to. "
        "They are used strictly as a factual reference - exam structure, domain names and "
        "weightings, and service behaviour, all of which are facts rather than expression "
        "- and every question, option, distractor and explanation in this file is this "
        "project's own work. That is the opposite situation from cka, whose CNCF "
        "curriculum source was CC-BY licensed and therefore ingestible with attribution. "
        "Consequently there is no third-party licence to inherit and no attribution field "
        "is required; the trademark position is separate and is recorded in "
        "meta.trademark_note."
    ),
}


def main():
    fails = []

    doc = {"meta": dict(META), "questions": []}

    seen_ids = set()
    tdist, keydist, pointdist = {}, {}, {}
    high_stakes = grundstoff = 0

    for q in QUESTIONS:
        if q["id"] in seen_ids:
            fails.append("%s: duplicate id" % q["id"])
        seen_ids.add(q["id"])

        # every locale present, with the same option set
        opt_keys = None
        for loc in LOCALES:
            if loc not in q["text"] or loc not in q["explanation"]:
                fails.append("%s: locale %s missing" % (q["id"], loc))
                continue
            keys = sorted(q["text"][loc]["options"])
            if opt_keys is None:
                opt_keys = keys
            elif keys != opt_keys:
                fails.append("%s: option keys differ in %s" % (q["id"], loc))
            if not q["text"][loc]["question"].strip():
                fails.append("%s: empty question in %s" % (q["id"], loc))
            if len(q["explanation"][loc].strip()) < 40:
                fails.append("%s: explanation too short in %s" % (q["id"], loc))
            for k, v in q["text"][loc]["options"].items():
                if not v.strip():
                    fails.append("%s: empty option %s in %s" % (q["id"], k, loc))

        # answer key sanity
        for c in q["correct"]:
            if c not in opt_keys:
                fails.append("%s: correct answer %r not an option" % (q["id"], c))
        if q["question_type"] == SC:
            if len(q["correct"]) != 1:
                fails.append("%s: single_choice with %d correct answers"
                             % (q["id"], len(q["correct"])))
            if len(opt_keys) != 4:
                fails.append("%s: single_choice should have 4 options, has %d"
                             % (q["id"], len(opt_keys)))
        elif q["question_type"] == MC:
            # AWS defines multiple response as two or more correct out of five or
            # more options; the pilot follows that shape rather than inventing one.
            if len(q["correct"]) < 2:
                fails.append("%s: multi_choice with fewer than 2 correct answers"
                             % q["id"])
            if len(opt_keys) < 5:
                fails.append("%s: multi_choice should have at least 5 options, has %d"
                             % (q["id"], len(opt_keys)))
        else:
            fails.append("%s: unknown question_type %r" % (q["id"], q["question_type"]))

        # points follow grundstoff, per the cka convention
        expected_points = 1 if q["grundstoff"] else 2
        if q["points"] != expected_points:
            fails.append("%s: points %d does not follow grundstoff" % (q["id"], q["points"]))

        if q["topic_code"] not in DOMAINS:
            fails.append("%s: unknown topic_code %r" % (q["id"], q["topic_code"]))
        if "verified against" not in q["legal_basis"]:
            fails.append("%s: legal_basis names no verification source" % q["id"])
        if "Task Statement" not in q["legal_basis"]:
            fails.append("%s: legal_basis names no task statement" % q["id"])

        tdist[q["topic_code"]] = tdist.get(q["topic_code"], 0) + 1
        pointdist[q["points"]] = pointdist.get(q["points"], 0) + 1
        high_stakes += 1 if q["high_stakes"] else 0
        grundstoff += 1 if q["grundstoff"] else 0
        for c in q["correct"]:
            keydist[c] = keydist.get(c, 0) + 1

        doc["questions"].append({k: q[k] for k in KEY_ORDER})

    n = len(doc["questions"])

    # ---- constraint 1 tripwire -----------------------------------------
    # No QUESTION may name a commercial exam-prep vendor or a dump site. The
    # meta block is exempt because meta.not_used_as_sources has to be able to
    # name what was deliberately avoided. This is a mechanical check, not a
    # substitute for the sourcing discipline in the module docstring.
    qblob = json.dumps(doc["questions"], ensure_ascii=False).lower()
    for banned in ("braindump", "brain dump", "exam dump", "tutorials dojo",
                   "whizlabs", "udemy", "examtopics", "skillcertpro",
                   "digital cloud training", "stephane maarek", "adrian cantrill"):
        if banned in qblob:
            fails.append("question content mentions banned source %r" % banned)

    # ---- the cka disclaimer must NOT be carried over -------------------
    # cka says it is not an exam simulator because its exam is hands-on. SAA is
    # MCQ-only, so repeating that framing here would be a factual error about
    # AWS. Guard against a future copy-paste.
    for phrase in ("100% hands-on", "100% performance-based",
                   "performance-based exam"):
        for q in doc["questions"]:
            if phrase in json.dumps(q, ensure_ascii=False).lower():
                fails.append("%s: carries cka's hands-on disclaimer, which is false "
                             "for SAA-C03" % q["id"])

    # ---- domain distribution against AWS's published weightings --------
    for code, spec in DOMAINS.items():
        got = tdist.get(code, 0)
        share = 100.0 * got / n
        drift = abs(share - spec["weight"])
        if drift > 1.5:
            fails.append("%s: %d/%d = %.1f%% drifts %.1f points from AWS's published "
                         "%d%%" % (code, got, n, share, drift, spec["weight"]))

    # ---- meta sanity ---------------------------------------------------
    m = doc["meta"]
    m["total_questions"] = n
    m["topic_distribution"] = {code: tdist.get(code, 0) for code in DOMAINS}
    m["multi_response_questions"] = sum(
        1 for q in doc["questions"] if q["question_type"] == MC)

    for required in ("license", "license_url", "license_note", "legal_review_status",
                     "draft_note", "sources", "description", "locale_note",
                     "exam_format_note", "topic_weighting_note", "pass_rule_note",
                     "trademark_note", "not_used_as_sources", "renewal_note"):
        if not m.get(required):
            fails.append("meta.%s missing or empty" % required)
    if m["license"] != "CC BY-NC-SA 4.0":
        fails.append("meta.license is not CC BY-NC-SA 4.0")
    if m["canonical_locale"] != "en" or m["locales"] != ["en", "de", "ja", "zh"]:
        fails.append("locale set deviates from the cka precedent without a note")
    if "cka" not in m["locale_note"]:
        fails.append("meta.locale_note does not record the cka precedent")
    if sum(m["topic_distribution"].values()) != n:
        fails.append("meta.topic_distribution does not sum to the question count")
    if "SAA-C03" not in m["description"]:
        fails.append("meta.description does not name the exam code")
    if "not affiliated" not in m["description"].lower():
        fails.append("meta.description does not disclaim AWS affiliation")

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    print("wrote %s (%d questions)" % (OUT, n))
    print("domain distribution:")
    for code, spec in DOMAINS.items():
        got = tdist.get(code, 0)
        print("  %-32s %2d  %5.1f%%  (AWS publishes %d%%)"
              % (code, got, 100.0 * got / n, spec["weight"]))
    print("question types:      single_choice=%d  multi_choice=%d"
          % (sum(1 for q in doc["questions"] if q["question_type"] == SC),
             sum(1 for q in doc["questions"] if q["question_type"] == MC)))
    print("answer key spread:   %s" % dict(sorted(keydist.items())))
    print("points distribution: %s" % dict(sorted(pointdist.items())))
    print("high_stakes: %d   grundstoff: %d" % (high_stakes, grundstoff))
    print("locales:             %s (canonical %s)" % (LOCALES, META["canonical_locale"]))

    if fails:
        print("\nFAILURES:")
        for f in fails:
            print("  - %s" % f)
        sys.exit(1)
    print("\nall integrity checks passed")


if __name__ == "__main__":
    main()
