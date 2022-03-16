FROM registry.gitlab.com/onti-fintech/onti-2022-fintech/fintech2022004/mall/bardinpetr/frontend-base:latest

COPY ./ ./

RUN npm run build

EXPOSE 82

CMD ["npm", "run", "serve"]